"""Unit 18: independently fixed byte-checker acceptance and rejection obligations.

DESIGN 4.15 / TEST_PLAN IQ1--IQ20 / ORACLE-133--137 govern. The embedded
Phase C reference and fixture transports are test-only and never imported by
production. No expected verdict comes from the checker. The unconditional
checker import is the intended Phase D RED until production exists.
"""

from __future__ import annotations

import ast
import builtins
import dis
import hashlib
import inspect
import io
import json
import os
import subprocess
import sys
import types
from collections import Counter
from pathlib import Path
from typing import get_type_hints

import pytest

# isort: split
import exactfrac_verify.check as checker

# isort: split

import exactfrac.certificate as producer
import exactfrac.solve as solver
from exactfrac.instance import Instance
from exactfrac.solve import SolveResult
from exactfrac.witness import ExactValue, Witness

_ROOT = Path(__file__).resolve().parents[1]
_CATALOGUE = _ROOT / "docs/ORACLE_CATALOG.md"
_CATALOGUE_BYTES = 3_312_641
_CATALOGUE_SHA = "05255f65148c007278a38df664df5e6ff02db868d63fdafe7d9a016861952840"
_CHECKER_PATH = _ROOT / "exactfrac_verify/check.py"
_ROUTES = ("Standard", "Accelerated")

# Exact private Phase C sources; embedded strings are not checker implementation.
_INDEPENDENT_WIRE_SOURCE = '"""Phase C test-only byte-pair oracle; not Unit 18 production code.\n\nNo ExactFrac imports, no production helpers, no file I/O and no expected answers.\nThe public-to-this-private-module verification function accepts only two bytes objects.\nA lexical certificate grammar is checked without re-encoding the decoded object.\n"""\nimport json\nimport re\n\n_NUM = rb\'(?:0|[1-9][0-9]*)\'\n_POS = rb\'(?:[1-9][0-9]*)\'\n_U = rb\'\\[\' + _NUM + rb\'(?:,\' + _NUM + rb\')*\\]\'\n_PAIR = rb\'\\[\' + _NUM + rb\',\' + _POS + rb\'\\]\'\n_Y = rb\'\\[(?:\' + _PAIR + rb\'(?:,\' + _PAIR + rb\')*)?\\]\'\n_EMPTY = rb\'\\{"format":"exactfrac-certificate/1","empty":true,"N":\' + _NUM + rb\',"D":\' + _POS + rb\'\\}\\n\'\n_NONEMPTY = (rb\'\\{"format":"exactfrac-certificate/1","empty":false,"N":\' + _NUM\n            + rb\',"D":\' + _POS + rb\',"U":\' + _U + rb\',"y":\' + _Y + rb\'\\}\\n\')\n_CERTIFICATE = re.compile(rb\'(?:\' + _EMPTY + rb\'|\' + _NONEMPTY + rb\')\')\n_INTEGER = re.compile(r\'(?:0|-?[1-9][0-9]*)\')\n\n\ndef _require(condition, reason):\n    if not condition:\n        raise ValueError(reason)\n\n\ndef _decimal(token):\n    _require(_INTEGER.fullmatch(token) is not None, \'noncanonical integer token\')\n    negative = token.startswith(\'-\')\n    digits = token[1:] if negative else token\n    value = 0\n    # No full-token int conversion; each conversion is at most seven digits.\n    for position in range(0, len(digits), 7):\n        chunk = digits[position:position + 7]\n        value = value * (10 ** len(chunk)) + int(chunk)\n    return -value if negative else value\n\n\ndef _no_noninteger(_token):\n    raise ValueError(\'noninteger number token\')\n\n\ndef _object(pairs):\n    result = {}\n    for key, value in pairs:\n        _require(key not in result, \'duplicate decoded key\')\n        result[key] = value\n    return result\n\n\ndef _parse(raw):\n    _require(type(raw) is bytes, \'serialized input must be exact bytes\')\n    _require(not raw.startswith(b\'\\xef\\xbb\\xbf\'), \'UTF-8 BOM forbidden\')\n    try:\n        text = raw.decode(\'utf-8\')\n    except UnicodeDecodeError as exc:\n        raise ValueError(\'invalid UTF-8\') from exc\n    try:\n        return json.loads(text, object_pairs_hook=_object, parse_int=_decimal,\n                          parse_float=_no_noninteger, parse_constant=_no_noninteger)\n    except json.JSONDecodeError as exc:\n        raise ValueError(\'invalid JSON document\') from exc\n\n\ndef parse_instance(raw):\n    """Decode and validate canonical graph data; do not sort or aggregate."""\n    data = _parse(raw)\n    _require(type(data) is dict, \'instance must be object\')\n    keys = set(data)\n    _require(keys in ({\'format\', \'n\', \'edges\', \'f\'},\n                      {\'format\', \'n\', \'edges\', \'f\', \'labels\'}), \'instance fields\')\n    _require(type(data[\'format\']) is str and data[\'format\'] == \'exactfrac-instance/1\',\n             \'instance format\')\n    n = data[\'n\']\n    _require(type(n) is int and n >= 1, \'positive integer n\')\n    f = data[\'f\']\n    _require(type(f) is list and len(f) == n, \'f length/type\')\n    _require(all(type(x) is int and x >= 1 for x in f), \'positive integer f\')\n    if \'labels\' in data:\n        labels = data[\'labels\']\n        _require(type(labels) is list and len(labels) == n, \'labels length/type\')\n        _require(all(type(x) in (int, str) for x in labels), \'label exact types\')\n        _require(len(set(labels)) == len(labels), \'duplicate labels\')\n    edges = data[\'edges\']\n    _require(type(edges) is list and len(edges) > 0, \'nonempty support\')\n    degrees = [0] * n\n    previous = None\n    for edge in edges:\n        _require(type(edge) is list and len(edge) == 3, \'edge shape\')\n        u, v, q = edge\n        _require(all(type(x) is int for x in edge), \'integer edge fields\')\n        _require(0 <= u < v < n and q >= 1, \'edge range/orientation/multiplicity\')\n        _require(previous is None or previous < (u, v), \'strict canonical edge order\')\n        previous = (u, v)\n        degrees[u] += q\n        degrees[v] += q\n    _require(all(cap <= degree for cap, degree in zip(f, degrees)), \'active condition\')\n    return data\n\n\ndef verify(instance_bytes, certificate_bytes):\n    """Independently return a decoded certificate iff admissible/raw-attaining or Empty.\n\n    Validation of the complete instance precedes parsing the certificate and hence\n    precedes every interpretation of an edge reference. No optimality is asserted.\n    """\n    instance = parse_instance(instance_bytes)\n    _require(type(certificate_bytes) is bytes, \'certificate must be exact bytes\')\n    _require(_CERTIFICATE.fullmatch(certificate_bytes) is not None, \'certificate wire grammar\')\n    cert = _parse(certificate_bytes)\n    # Grammar checks precede object creation; duplicate/escaped/reordered keys cannot match.\n    _require(type(cert) is dict, \'certificate object\')\n    _require(type(cert[\'empty\']) is bool and type(cert[\'N\']) is int and type(cert[\'D\']) is int,\n             \'certificate field types\')\n    _require(cert[\'N\'] >= 0 and cert[\'D\'] > 0, \'certificate signs\')\n    if cert[\'empty\']:\n        _require(sum(edge[2] for edge in instance[\'edges\']) == 1, \'false Empty\')\n        _require((cert[\'N\'], cert[\'D\']) == (0, 1), \'literal Empty pair\')\n        return cert\n    U = cert[\'U\']\n    _require(type(U) is list and bool(U), \'nonempty U\')\n    _require(all(type(v) is int and 0 <= v < instance[\'n\'] for v in U), \'vertex range/type\')\n    _require(all(a < b for a, b in zip(U, U[1:])), \'strict U order\')\n    shore = set(U)\n    y = cert[\'y\']\n    _require(type(y) is list, \'sparse list\')\n    previous = -1\n    selected = 0\n    for entry in y:\n        _require(type(entry) is list and len(entry) == 2, \'sparse pair shape\')\n        ref, count = entry\n        _require(type(ref) is int and type(count) is int, \'sparse exact integers\')\n        _require(previous < ref < len(instance[\'edges\']), \'sparse reference order/range\')\n        previous = ref\n        u, v, q = instance[\'edges\'][ref]\n        _require(0 < count <= q, \'sparse positive bounded count\')\n        _require((u in shore) != (v in shore), \'sparse crossing constraint\')\n        selected += count\n    s = sum(instance[\'f\'][v] for v in U)\n    e = sum(q for u, v, q in instance[\'edges\'] if u in shore and v in shore)\n    _require((s + selected) % 2 == 1, \'odd admissibility\')\n    _require(s + selected >= 3, \'minimum admissibility\')\n    _require(cert[\'N\'] == 2 * (e + selected), \'literal numerator\')\n    _require(cert[\'D\'] == s + selected - 1, \'literal denominator\')\n    return cert\n'  # noqa: E501
_FIXTURE_SUPPORT_SOURCE = '"""Private Phase C catalogue/derivation utilities, never production verifier helpers."""\nimport ast\nimport hashlib\nimport itertools\nimport json\nfrom pathlib import Path\n\nSYMBOLS = {\'T\': 10**4800, \'Tm1\':10**4800-1, \'Tp1\':10**4800+1,\n           \'twoT\':2*10**4800, \'twoTm2\':2*10**4800-2, \'minusT\':-(10**4800)}\n\ndef number(x):\n    if type(x) is tuple and len(x)==2 and x[0]==\'sym\':\n        return SYMBOLS[x[1]]\n    if type(x) is not int:\n        raise ValueError(\'not an integer/symbol fixture\')\n    return x\n\ndef compact_number(x):\n    for name,value in SYMBOLS.items():\n        if x==value:return (\'sym\',name)\n    return x\n\ndef read_tables(path, prefixes=(\'U15_INPUTS\',\'U16_INPUTS\',\'U15_GLOBAL\',\'U15_BASELINES\',\n                               \'U15_H2\',\'U15_SHORES\',\'U17_\')):\n    tables={}; current=None; header=False\n    for line in Path(path).read_text(encoding=\'utf-8\').splitlines():\n        if line.startswith(\'### Fixture table: \'):\n            name=line.split(\': \',1)[1]\n            current=name if any(name.startswith(p) for p in prefixes) else None\n            if current:\n                if name in tables:raise ValueError(\'duplicate table \'+name)\n                tables[name]=[];header=True\n        elif current and line.startswith(\'| \'):\n            cells=[v.strip() for v in line[1:-1].split(\'|\')]\n            if header:header=False\n            elif not all(v==\'---\' for v in cells):\n                if not all(v.startswith(\'`\') and v.endswith(\'`\') for v in cells):\n                    raise ValueError(\'nonliteral fixture cell\')\n                tables[current].append(tuple(ast.literal_eval(v[1:-1]) for v in cells))\n        elif current and line.strip():current=None\n    return tables\n\ndef digits(value):\n    negative=value<0; value=abs(value)\n    if value==0:return b\'0\'\n    pieces=[]\n    while value:\n        value,remainder=divmod(value,100000)\n        pieces.append(remainder)\n    output=str(pieces.pop()).encode(\'ascii\')\n    output+=b\'\'.join((\'%05d\'%v).encode(\'ascii\') for v in reversed(pieces))\n    return (b\'-\' if negative else b\'\')+output\n\ndef encode(value):\n    """Untrusted test transport encoder; NOT the expected-byte recipe nor verifier."""\n    if value is None:return b\'null\'\n    if type(value) is bool:return b\'true\' if value else b\'false\'\n    if type(value) is int:return digits(value)\n    if type(value) is str:return json.dumps(value,ensure_ascii=True).encode(\'ascii\')\n    if type(value) in (list,tuple):return b\'[\'+b\',\'.join(encode(x) for x in value)+b\']\'\n    if type(value) is dict:return b\'{\'+b\',\'.join(encode(k)+b\':\'+encode(v) for k,v in value.items())+b\'}\'\n    raise ValueError(\'transport type\')\n\ndef fingerprint(rows):\n    return hashlib.sha256(b\'\'.join(encode(row)+b\'\\n\' for row in rows)).hexdigest()\n\ndef registry(tables):\n    records=[]\n    for key,kind,n,edges,f,labels in tables[\'U15_INPUTS\']:\n        records.append((\'U15_INPUTS/\'+key,{\'format\':\'exactfrac-instance/1\',\'n\':n,\n                        \'edges\':[list(e) for e in edges],\'f\':list(f),\n                        **({} if labels is None else {\'labels\':list(labels)})}))\n    for key,n,edges,f,labels in tables[\'U16_INPUTS\']:\n        records.append((\'U16_INPUTS/\'+key,{\'format\':\'exactfrac-instance/1\',\'n\':n,\n                        \'edges\':[list(e) for e in edges],\'f\':list(f),\n                        **({} if labels is None else {\'labels\':list(labels)})}))\n    for key,n,edges,f,labels in tables.get(\'U17_INPUTS\',[]):\n        lab=None if labels is None else [number(x) if type(x) is tuple else x for x in labels]\n        records.append((\'U17_INPUTS/\'+key,{\'format\':\'exactfrac-instance/1\',\'n\':n,\n                       \'edges\':[[u,v,number(q)] for u,v,q in edges],\'f\':[number(x) for x in f],\n                       **({} if lab is None else {\'labels\':lab})}))\n    if len({k for k,_ in records})!=len(records):raise ValueError(\'duplicate registry identity\')\n    return records\n\ndef recipe(parts):\n    result=[]\n    for part in parts:\n        if type(part) is str:result.append(part.encode(\'ascii\'))\n        elif type(part) is tuple and len(part)==3 and part[0]==\'repeat\':\n            char,count=part[1:]\n            if type(char) is not str or len(char)!=1 or type(count) is not int or count<0:\n                raise ValueError(\'bad repeat\')\n            result.append(char.encode(\'ascii\')*count)\n        else:raise ValueError(\'bad byte recipe\')\n    return b\'\'.join(result)\n\ndef witness_certificate(U,y,N,D):\n    obj={\'format\':\'exactfrac-certificate/1\',\'empty\':U is None,\'N\':N,\'D\':D}\n    if U is not None:obj.update(U=list(U),y=[list(x) for x in y])\n    return obj\n\ndef raw_value(graph,U,y):\n    """Direct independent primitive evaluation for derivation, not byte validation."""\n    s=sum(graph[\'f\'][v] for v in U)\n    Y=sum(count for _,count in y)\n    e=sum(q for u,v,q in graph[\'edges\'] if u in U and v in U)\n    b=sum(q for u,v,q in graph[\'edges\'] if (u in U)!=(v in U))\n    return 2*(e+Y),s+Y-1,(s,e,b,Y)\n\ndef realize(graph,U,Y):\n    y=[]\n    for ref,(u,v,q) in enumerate(graph[\'edges\']):\n        if (u in U)!=(v in U):\n            take=min(q,Y);Y-=take\n            if take:y.append((ref,take))\n    if Y:raise ValueError(\'unrealizable total\')\n    return tuple(y)\n\ndef global_reference(graph,mode=\'endpoints\'):\n    """Exhaustive finite private oracle; no production branch algorithm is reproduced.\n\n    Full-vector/scalar enumeration is used only on declared finite small cases.\n    Endpoint mode scans 2^n-1 shores but never scans q, f or Q copies.\n    """\n    best=None\n    for mask in range(1,1<<graph[\'n\']):\n        U=tuple(v for v in range(graph[\'n\']) if mask & (1<<v))\n        s=sum(graph[\'f\'][v] for v in U)\n        e=sum(q for u,v,q in graph[\'edges\'] if u in U and v in U)\n        boundary=[(ref,q) for ref,(u,v,q) in enumerate(graph[\'edges\']) if (u in U)!=(v in U)]\n        b=sum(q for _,q in boundary)\n        if mode==\'vectors\':\n            items=((sum(counts),tuple((ref,t) for (ref,_),t in zip(boundary,counts) if t))\n                   for counts in itertools.product(*(range(q+1) for _,q in boundary)))\n        else:\n            low=2 if s==1 else (1 if s%2==0 else 0)\n            high=b-((s+b+1)%2)\n            totals=range(b+1) if mode==\'scalars\' else ((low,) if high==low else (low,high))\n            items=((t,None) for t in totals if 0<=t<=b)\n        for Y,y in items:\n            if (s+Y)%2!=1 or s+Y<3:continue\n            N,D=2*(e+Y),s+Y-1\n            if best is None or N*best[1]>best[0]*D:\n                best=(N,D,U,realize(graph,U,Y) if y is None else y)\n    return (0,1,None,None) if best is None else best\n\ndef same_value(a,b):return a[0]*b[1]==b[0]*a[1]\n\ndef small_for_exhaustion(graph):return max(q for _,_,q in graph[\'edges\'])<=6\n'  # noqa: E501
_FIXTURE_MUTATIONS_SOURCE = '"""Execute catalogue-declared wire adversaries; no production interaction."""\nimport json\nfrom fixture_support import encode\nfrom independent_wire import _parse\n\ndef mutate(raw,operations):\n    for operation in operations:\n        op=operation[0]\n        if op in (\'set\',\'delete\'):\n            document=_parse(raw)\n            target=document\n            for part in operation[1][:-1]:target=target[part]\n            if op==\'set\':target[operation[1][-1]]=operation[2]\n            else:del target[operation[1][-1]]\n            raw=encode(document)+(b\'\\n\' if raw.endswith(b\'\\n\') else b\'\')\n        elif op==\'replace\':\n            a,b=operation[1].encode(\'utf-8\'),operation[2].encode(\'utf-8\')\n            if raw.count(a)!=1:raise ValueError(\'replacement not unique: \'+operation[1])\n            raw=raw.replace(a,b)\n        elif op==\'prefix\':raw=operation[1].encode(\'utf-8\')+raw\n        elif op==\'prefix_hex\':raw=bytes.fromhex(operation[1])+raw\n        elif op==\'suffix\':raw+=operation[1].encode(\'utf-8\')\n        elif op==\'strip_final_lf\':\n            if not raw.endswith(b\'\\n\'):raise ValueError(\'no LF\')\n            raw=raw[:-1]\n        elif op==\'reverse_keys\':\n            d=_parse(raw);raw=encode(dict(reversed(list(d.items()))))+(b\'\\n\' if raw.endswith(b\'\\n\') else b\'\')\n        elif op==\'pretty\':raw=json.dumps(_parse(raw),ensure_ascii=True,indent=2).encode(\'ascii\')+b\'\\n\'\n        elif op==\'utf8_strings\':raw=json.dumps(_parse(raw),ensure_ascii=False,separators=(\',\',\':\')).encode(\'utf-8\')\n        elif op==\'quote_field\':\n            name=operation[1];token=b\'"\'+name.encode()+b\'":\';start=raw.index(token)+len(token)\n            end=start\n            while end<len(raw) and 48<=raw[end]<=57:end+=1\n            raw=raw[:start]+b\'"\'+raw[start:end]+b\'"\'+raw[end:]\n        else:raise ValueError(\'unknown mutation operation\')\n    return raw\n'  # noqa: E501
_UNIT18_SUPPORT_SOURCE = '"""Private Unit 18 fixture assembly. No checker code; no production imports.\n\nTables, byte recipes and independent mathematical references are the authority.\nThis module is a test transport, never the expected verdict\'s derivation.\n"""\nfrom pathlib import Path\nimport hashlib\nfrom fixture_support import (read_tables, registry, encode, number, recipe, fingerprint)\nfrom fixture_mutations import mutate\n\nPREFIX_LENGTH = 3_212_040\nPREFIX_SHA = \'04ef6a4b38463aecb0d86731d1873aadb4acb8bc8a8593e0ea82b4325e56e7ac\'\nOLD_TEST_SHA = \'c70f7120fe10d07668fc37624843cc77a02ef58244fbda432d04591123042724\'\nOLD_GUARD = b\'    assert _sha(_CATALOGUE.read_bytes()) == _CATALOGUE_SHA\\n\'\nNEW_GUARD = (b\'    catalogue_bytes = _CATALOGUE.read_bytes()\\n\'\n             b\'    assert len(catalogue_bytes) >= 3_212_040\\n\'\n             b\'    assert _sha(catalogue_bytes[:3_212_040]) == _CATALOGUE_SHA\\n\')\nABSENCE = b\'    assert not (_ROOT / "exactfrac_verify/check.py").exists()\\n\'\n\ndef tables_at(path):\n    return read_tables(path, (\'U15_INPUTS\',\'U16_INPUTS\',\'U15_GLOBAL\',\'U15_BASELINES\',\n                             \'U15_H2\',\'U15_SHORES\',\'U17_\',\'U18_\'))\n\ndef all_graphs(tables):\n    answer = registry(tables)\n    for key,n,edges,f,labels in tables[\'U18_INPUTS\']:\n        answer.append((\'U18_INPUTS/\'+key, {\'format\':\'exactfrac-instance/1\',\'n\':n,\n              \'edges\':[[u,v,number(q)] for u,v,q in edges], \'f\':[number(x) for x in f],\n              **({} if labels is None else {\'labels\':list(labels)})}))\n    if len({k for k,g in answer}) != len(answer):\n        raise AssertionError(\'Duplicate qualified registry identity\')\n    return answer\n\ndef literals(tables):\n    graphs = dict(all_graphs(tables)); out = {}\n    for table,prefix in ((\'U17_BYTES\',\'U17/\'),(\'U18_LITERALS\',\'U18/\')):\n        for row in tables[table]:\n            key,gid,kind,U,y,N,D,parts,size,digest = row\n            wire = recipe(parts)\n            if len(wire)!=size or hashlib.sha256(wire).hexdigest()!=digest:\n                raise AssertionError(\'Literal identity \'+key)\n            out[prefix+key] = (encode(graphs[gid]),wire,row)\n    return out\n\ndef byte_edit(raw, operations):\n    for op in operations:\n        if op[0]==\'raw_hex\': raw = bytes.fromhex(op[1])\n        elif op[0]==\'truncate\': raw = raw[:op[1]]\n        elif op[0]==\'replace_hex\':\n            old,new = bytes.fromhex(op[1]),bytes.fromhex(op[2])\n            if raw.count(old)!=1: raise AssertionError(\'Hex replacement not unique\')\n            raw=raw.replace(old,new)\n        elif op[0]==\'encoding\':\n            raw=raw.decode(\'utf-8\').encode(op[1])\n        else: raw = mutate(raw,(op,))\n    return raw\n\ndef wire_cases(tables):\n    fixed=literals(tables); cases=[]\n    for key,(ib,cb,row) in fixed.items():\n        cases.append((key,ib,cb,True,\'literal\'))\n    for name,good in ((\'U17_WIRE_REJECT\',False),(\'U17_WIRE_ACCEPT\',True)):\n        for row in tables[name]:\n            if good:key,bid,stream,ops,size,digest=row\n            else:key,bid,stream,ops,reason,equal,size,digest=row\n            ib,cb,_=fixed[\'U17/\'+bid]; changed=byte_edit(ib if stream==\'instance\' else cb,ops)\n            if len(changed)!=size or hashlib.sha256(changed).hexdigest()!=digest:\n                raise AssertionError(\'Inherited byte row \'+key)\n            cases.append((\'U17/\'+key,changed if stream==\'instance\' else ib,\n                          changed if stream==\'certificate\' else cb,good,\'inherited\'))\n    for key,bid,stream,ops,good,reason,size,digest in tables[\'U18_WIRE_CASES\']:\n        ib,cb,_=fixed[bid]; changed=byte_edit(ib if stream==\'instance\' else cb,ops)\n        if len(changed)!=size or hashlib.sha256(changed).hexdigest()!=digest:\n            raise AssertionError(\'Unit18 byte row \'+key)\n        cases.append((\'U18/\'+key,changed if stream==\'instance\' else ib,\n                      changed if stream==\'certificate\' else cb,good,reason))\n    if len({c[0] for c in cases})!=len(cases):raise AssertionError(\'Duplicate wire identity\')\n    return cases\n\ndef guarded_prefix(raw):\n    if len(raw)<PREFIX_LENGTH:raise ValueError(\'Catalogue shorter than protected prefix\')\n    if hashlib.sha256(raw[:PREFIX_LENGTH]).hexdigest()!=PREFIX_SHA:\n        raise ValueError(\'Historical catalogue bytes changed\')\n\ndef exact_test_transition(old,new):\n    if hashlib.sha256(old).hexdigest()!=OLD_TEST_SHA:raise AssertionError(\'Original Unit17 test identity\')\n    if old.count(OLD_GUARD)!=1 or old.count(ABSENCE)!=2:raise AssertionError(\'Original guard/absence census\')\n    if new != old.replace(OLD_GUARD,NEW_GUARD,1):raise AssertionError(\'Unauthorized test byte change\')\n    if new.count(ABSENCE)!=2:raise AssertionError(\'Phase D absence line retired early\')\n    return True\n'  # noqa: E501

_EMBEDDED_SHA = {
    'independent_wire': '95c1031fc387b765569fc381062384b8919a79f12128883becfc11ad7236bff6',
    'fixture_support': '1e5ef183cf99b7af88852027a8435cbd06c4db37e99fcc21a73edbc51edbc142',
    'fixture_mutations': '100b6c804e90835d73f36181ddd6255d5fc59537e1e324e0393fcea9a05ca3cd',
    'unit18_support': 'c546885198b658a589f0b949e3e35b33cb98ac59472a0d093503d715292a096a',
}


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _test_tools():
    """Separate namespaces; no sys.modules alias or production parsing shared."""
    modules = {}
    original_import = builtins.__import__

    def local_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name in modules:
            return modules[name]
        if name.split(".")[0] in {"exactfrac", "exactfrac_verify"}:
            raise ImportError("Production import in independent test route")
        return original_import(name, globals, locals, fromlist, level)

    for name, source in (
        ("independent_wire", _INDEPENDENT_WIRE_SOURCE),
        ("fixture_support", _FIXTURE_SUPPORT_SOURCE),
        ("fixture_mutations", _FIXTURE_MUTATIONS_SOURCE),
        ("unit18_support", _UNIT18_SUPPORT_SOURCE),
    ):
        assert _sha(source.encode()) == _EMBEDDED_SHA[name]
        module = types.ModuleType("_unit18_private_" + name)
        module.__dict__["__builtins__"] = {**vars(builtins), "__import__": local_import}
        exec(compile(source, "<unit18-test-only-" + name + ">", "exec"), module.__dict__)
        modules[name] = module
    return modules


_TOOLS = _test_tools()
_REF = _TOOLS["independent_wire"]
_FIX = _TOOLS["fixture_support"]
_SUPPORT = _TOOLS["unit18_support"]
_TABLES = _SUPPORT.tables_at(_CATALOGUE)
_REGISTRY = _SUPPORT.all_graphs(_TABLES)
_LITERALS = _SUPPORT.literals(_TABLES)
_CASES = _SUPPORT.wire_cases(_TABLES)
_CASE_BY_ID = {row[0]: row for row in _CASES}
_EXPECTED_GLOBALS = {
    row[0]: (_FIX.number(row[1]), _FIX.number(row[2]))
    for row in (*_TABLES["U17_GLOBALS"], *_TABLES["U18_GLOBALS"])
}


def _invalid(function, *args, **kwargs):
    with pytest.raises(ValueError) as caught:
        function(*args, **kwargs)
    assert type(caught.value) is ValueError


def _instance(graph):
    return Instance(
        graph["n"], tuple(tuple(edge) for edge in graph["edges"]), tuple(graph["f"]),
        None if "labels" not in graph else tuple(graph["labels"]),
    )


def _literal_object(row):
    result = {"format": "exactfrac-certificate/1", "empty": row[3] is None,
              "N": _FIX.number(row[5]), "D": _FIX.number(row[6])}
    if row[3] is not None:
        result.update(U=list(row[3]), y=[[ref, _FIX.number(count)] for ref, count in row[4]])
    return result


def test_closed_tables_and_qualified_registry_are_preserved():
    raw = _CATALOGUE.read_bytes()
    assert len(raw) >= _CATALOGUE_BYTES
    assert _sha(raw[:_CATALOGUE_BYTES]) == _CATALOGUE_SHA
    for group in ("U17", "U18"):
        rows = _TABLES[group + "_FINGERPRINTS"]
        assert {row[0] for row in rows} == {
            name for name in _TABLES
            if name.startswith(group + "_") and name != group + "_FINGERPRINTS"
        }
        for name, count, digest in rows:
            assert len(_TABLES[name]) == count
            assert _FIX.fingerprint(_TABLES[name]) == digest
    for name, count, digest in _TABLES["U18_REGISTRY"]:
        assert len(_TABLES[name]) == count
        assert _FIX.fingerprint(_TABLES[name]) == digest
    census = dict(_TABLES["U18_CENSUS"])
    assert len(_REGISTRY) == census["registry_identities"] == 400
    assert len({key for key, _ in _REGISTRY}) == 400
    assert _FIX.fingerprint(_REGISTRY) == census["registry_fingerprint"]
    assert len(_REGISTRY) * len(_ROUTES) == census["real_solves_both_routes"] == 800
    assert len(_LITERALS) == 41
    assert len(_CASES) == 519
    assert sum(row[3] for row in _CASES) == 64
    assert len(_TABLES["U18_API_CASES"]) == 34
    assert len(_TABLES["U18_PRECEDENCE"]) == 12
    assert len(_TABLES["U18_EXCEPTIONS"]) == 8
    assert len(_TABLES["U18_MUTATIONS"]) == 24
    assert {row[0] for row in _TABLES["U18_MUTATIONS"]} == {
        f"Q{index:02d}" for index in range(1, 25)
    }


def test_public_api_success_and_root_ownership():
    assert type(checker.__all__) is tuple
    assert checker.__all__ == ("verify_certificate",)
    function = checker.verify_certificate
    parameters = inspect.signature(function).parameters
    assert tuple(parameters) == ("instance", "certificate")
    assert all(p.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
               and p.default is inspect.Parameter.empty for p in parameters.values())
    assert get_type_hints(function) == {
        "instance": bytes, "certificate": bytes, "return": type(None),
    }
    assert {name for name, value in vars(checker).items()
            if not name.startswith("_") and callable(value)} == {"verify_certificate"}
    assert (_ROOT / "exactfrac/__init__.py").read_bytes() == b""
    assert (_ROOT / "exactfrac_verify/__init__.py").read_bytes() == b""
    assert _sha((_ROOT / "exactfrac_verify/brute.py").read_bytes()) == (
        "b31e53a8b16a37ef8827141a78169ffe9b0a84762843a3ad45c89d9344f98bf6"
    )
    assert Path(checker.__file__).resolve() == _CHECKER_PATH


@pytest.mark.parametrize("key", tuple(_LITERALS))
def test_literal_fixtures_preserve_raw_fields_and_original_coordinates(key):
    ib, cb, row = _LITERALS[key]
    expected = _literal_object(row)
    assert _REF.verify(ib, cb) == expected
    assert (len(cb), _sha(cb)) == (row[8], row[9])
    for _ in range(3):
        assert checker.verify_certificate(ib, cb) is None
        assert checker.verify_certificate(instance=ib, certificate=cb) is None
    if not expected["empty"]:
        graph = _REF.parse_instance(ib)
        raw = _FIX.raw_value(graph, expected["U"], expected["y"])
        assert raw[:2] == (expected["N"], expected["D"])


@pytest.mark.parametrize("row", _CASES, ids=[row[0] for row in _CASES])
def test_all_fixed_wire_verdicts_against_separate_byte_reference(row):
    _, ib, cb, good, _ = row
    original = (ib, cb)
    if good:
        assert type(_REF.verify(ib, cb)) is dict
        assert checker.verify_certificate(ib, cb) is None
    else:
        _invalid(_REF.verify, ib, cb)
        _invalid(checker.verify_certificate, ib, cb)
    assert (ib, cb) == original


class _Poison:
    def __bytes__(self):
        raise AssertionError("Caller __bytes__ invoked")

    def __str__(self):
        raise AssertionError("Caller __str__ invoked")

    def __fspath__(self):
        raise AssertionError("Caller path conversion invoked")

    def read(self, *args, **kwargs):
        raise AssertionError("Caller stream read invoked")


class _BytesSubclass(bytes):
    def decode(self, *args, **kwargs):
        raise AssertionError("Bytes subclass decoded before exact-type validation")


def _api_bad(tag, raw, graph):
    inst = _instance(graph)
    witness = Witness(1, (0,) * inst.m)
    values = {
        "str": raw.decode(), "bytearray": bytearray(raw), "memoryview": memoryview(raw),
        "bytes-subclass": _BytesSubclass(raw), "None": None, "dict": {}, "list": [],
        "int": 1, "bool": True, "path-object": _Poison(), "stream": io.BytesIO(raw),
        "poison-__bytes__-object": _Poison(), "closed-Instance": inst,
        "closed-SolveResult": SolveResult(ExactValue(0, 1), None), "closed-Witness": witness,
    }
    return values[tag]


@pytest.mark.parametrize("row", _TABLES["U18_API_CASES"], ids=lambda row: row[0])
def test_registered_api_type_arity_and_keyword_cases(row):
    key, side, tag, _, _ = row
    ib, cb, _ = _LITERALS["U18/PAIR-FULL"]
    if side in ("instance", "certificate"):
        wrong = _api_bad(tag, ib if side == "instance" else cb, _REF.parse_instance(ib))
        _invalid(checker.verify_certificate, wrong if side == "instance" else ib,
                 wrong if side == "certificate" else cb)
        if isinstance(wrong, io.BytesIO):
            assert wrong.tell() == 0
    elif key == "ARITY-MISSING":
        with pytest.raises(TypeError):
            checker.verify_certificate(ib)
    elif key == "ARITY-EXTRA":
        with pytest.raises(TypeError):
            checker.verify_certificate(ib, cb, cb)
    elif key == "KEYWORD-CALL":
        assert checker.verify_certificate(instance=ib, certificate=cb) is None
    else:
        assert key == "SUCCESS-NONE"
        assert checker.verify_certificate(ib, cb) is None


def _trace_call(function, args, observer):
    """Opcode tracing is test instrumentation, not an added private checker API."""
    previous = sys.gettrace()
    instructions = {}

    def trace(frame, event, arg):
        if Path(frame.f_code.co_filename).resolve() == _CHECKER_PATH:
            frame.f_trace_opcodes = True
            if event == "opcode":
                code = frame.f_code
                if code not in instructions:
                    instructions[code] = {item.offset: item for item in dis.get_instructions(code)}
                observer(frame, instructions[code].get(frame.f_lasti))
            return trace
        return None

    try:
        sys.settrace(trace)
        return function(*args)
    finally:
        sys.settrace(previous)


def _certificate_access_trap(error, seen):
    public = checker.verify_certificate.__code__

    def observe(frame, instruction):
        if frame.f_code is public and instruction is not None:
            names = instruction.argrepr.translate(
                str.maketrans({char: " " for char in ",()[]\'\""})
            ).split()
            if instruction.opname.startswith("LOAD_FAST") and "certificate" in names:
                seen.append("certificate argument inspected")
                raise error
    return observe


def _precedence_input(tag):
    ib = _LITERALS["U18/PAIR-FULL"][0]
    graph = _REF.parse_instance(ib)
    if tag == "nonbytes":
        return _Poison()
    if tag == "syntax":
        return b"{"
    if tag == "duplicate-key":
        return ib.replace(b'"n":2', b'"n":2,"n":2')
    if tag == "outer-fields":
        graph["extra"] = 1
    elif tag == "n":
        graph["n"] = 0
    elif tag == "f":
        graph["f"] = []
    elif tag in ("labels", "malformed-labels-and-nonactive"):
        graph["labels"] = ["x", "x"]
        if tag == "malformed-labels-and-nonactive":
            graph["f"] = [99, 99]
    elif tag == "edge-shape":
        graph["edges"] = [[0, 1]]
    elif tag == "edge-order":
        graph["edges"] = [[1, 0, 3]]
    elif tag == "nonactive":
        graph["f"] = [99, 99]
    elif tag == "huge-n-short-f":
        graph["n"] = 10**4800
    else:
        assert tag in {"outer-fields", "n", "f"}
    return _FIX.encode(graph)


@pytest.mark.parametrize("row", _TABLES["U18_PRECEDENCE"], ids=lambda row: row[0])
def test_instance_rejection_precedes_any_certificate_argument_access(row):
    _, tag, _, _ = row
    cb = _LITERALS["U18/PAIR-FULL"][1]
    error = RuntimeError("premature certificate access")
    seen = []
    _invalid(_trace_call, checker.verify_certificate, (_precedence_input(tag), cb),
             _certificate_access_trap(error, seen))
    assert seen == []


def test_certificate_access_trace_has_a_positive_control():
    ib, cb, _ = _LITERALS["U18/PAIR-FULL"]
    error = MemoryError("certificate boundary fault")
    seen = []
    with pytest.raises(MemoryError) as caught:
        _trace_call(checker.verify_certificate, (ib, cb), _certificate_access_trap(error, seen))
    assert caught.value is error
    assert seen == ["certificate argument inspected"]


def _patch_json_operation(monkeypatch, replacement):
    # Discover imported function aliases by identity, never require a private name.
    functions = (json.loads, json.JSONDecoder.decode, json.JSONDecoder.raw_decode)
    for name, value in tuple(vars(checker).items()):
        if any(value is original for original in functions):
            monkeypatch.setattr(checker, name, replacement)
    monkeypatch.setattr(json, "loads", replacement)
    monkeypatch.setattr(json.JSONDecoder, "decode", replacement)
    monkeypatch.setattr(json.JSONDecoder, "raw_decode", replacement)


@pytest.mark.parametrize("row", _TABLES["U18_EXCEPTIONS"], ids=lambda row: row[0])
def test_registered_dependency_exception_identity_and_narrow_translation(row, monkeypatch):
    key, _, kind, _ = row
    ib, cb, _ = _LITERALS["U18/PAIR-FULL"]
    if key == "UTF8-SYNTAX":
        _invalid(checker.verify_certificate, b"\xff", cb)
        return
    if key == "RESOURCE-CERT":
        error = MemoryError("private parsing resource fault")
        seen = []
        with pytest.raises(MemoryError) as caught:
            _trace_call(checker.verify_certificate, (ib, cb), _certificate_access_trap(error, seen))
        assert caught.value is error and seen
        return
    error = (json.JSONDecodeError("synthetic syntax", "{", 1) if key == "JSON-SYNTAX"
             else getattr(builtins, kind)("dependency identity sentinel"))
    calls = []

    def raise_error(*args, **kwargs):
        calls.append(True)
        raise error

    _patch_json_operation(monkeypatch, raise_error)
    if key == "JSON-SYNTAX":
        _invalid(checker.verify_certificate, ib, cb)
    else:
        with pytest.raises(type(error)) as caught:
            checker.verify_certificate(ib, cb)
        assert caught.value is error
    assert calls


def test_bad_labels_reject_before_edge_degree_processing(monkeypatch):
    # Observe original decoded edge records/count identities, without naming locals.
    original = json.loads
    original_decode = json.JSONDecoder.decode
    observed = []
    watched = []
    done = []

    def remember(result):
        watched[:] = [*result["edges"], *(edge[2] for edge in result["edges"])]
        done.append(True)
        return result

    def decode(*args, **kwargs):
        return remember(original(*args, **kwargs))

    def decoder_method(*args, **kwargs):
        return remember(original_decode(*args, **kwargs))

    def trace_edges(frame, instruction):
        if done and any(value is item for value in frame.f_locals.values() for item in watched):
            observed.append("edge processing")
            raise RuntimeError("edge processing reached")

    for name, value in tuple(vars(checker).items()):
        if value is original:
            monkeypatch.setattr(checker, name, decode)
    monkeypatch.setattr(json, "loads", decode)
    monkeypatch.setattr(json.JSONDecoder, "decode", decoder_method)
    graph = {"format": "exactfrac-instance/1", "n": 2, "f": [100004, 100004],
             "labels": ["same", "same"], "edges": [[0, 1, 100003]]}
    cb = _LITERALS["U18/PAIR-FULL"][1]
    _invalid(_trace_call, checker.verify_certificate, (_FIX.encode(graph), cb), trace_edges)
    assert observed == []
    assert done
    graph["labels"] = ["left", "right"]
    graph["f"] = [1, 1]
    with pytest.raises(RuntimeError, match="edge processing reached"):
        _trace_call(checker.verify_certificate, (_FIX.encode(graph), cb), trace_edges)
    assert observed


def _one_emission_run(gid, graph, route):
    inst = _instance(graph)
    ib = _FIX.encode(graph)
    local = []

    def record(value, witness, origin):
        result = SolveResult(value, witness)
        obj = producer.build_certificate(inst, result)
        cb = producer.serialize_certificate(inst, obj)
        assert producer.serialize_certificate(inst, obj) == cb
        expected = {"format": "exactfrac-certificate/1", "empty": witness is None,
                    "N": value.N, "D": value.D}
        if witness is not None:
            expected.update(
                U=[v for v in range(inst.n) if witness.U & (1 << v)],
                y=[[ref, count] for ref, count in enumerate(witness.y) if count],
            )
        assert _REF.verify(ib, cb) == expected
        return (origin, cb, expected)

    baseline, endpoint, evaluate = solver._baseline, solver._endpoint, solver._evaluate

    def observe_baseline(*args):
        result = baseline(*args)
        local.append(record(*result, "Baseline"))
        return result

    def observe_endpoint(instance, branch, result):
        answer = endpoint(instance, branch, result)
        local.append(record(*answer, ("L0", "L1", "H0", "H1")[branch]))
        return answer

    def observe_evaluate(instance, witness):
        answer = evaluate(instance, witness)
        if sys._getframe(1).f_code is solver.solve.__code__:
            local.append(record(answer, witness, "H2"))
        return answer

    solver._baseline, solver._endpoint, solver._evaluate = (
        observe_baseline, observe_endpoint, observe_evaluate,
    )
    try:
        result, stats = solver.solve(inst, route)
    finally:
        solver._baseline, solver._endpoint, solver._evaluate = baseline, endpoint, evaluate
    final = record(result.value, result.witness, stats.attaining_candidate)
    return (gid, route, ib, final, tuple(local))


@pytest.fixture(scope="module")
def emissions():
    """One real solve per qualified identity and route; never deduplicate."""
    runs = [_one_emission_run(gid, graph, route)
            for gid, graph in _REGISTRY for route in _ROUTES]
    assert [(gid, route) for gid, route, *_ in runs] == [
        (gid, route) for gid, _ in _REGISTRY for route in _ROUTES
    ]
    assert len(runs) == 800
    return runs


@pytest.mark.parametrize("gid", [gid for gid, _ in _REGISTRY])
def test_both_real_solver_routes_and_all_local_reconstructions(gid, emissions):
    runs = [run for run in emissions if run[0] == gid]
    assert [run[1] for run in runs] == list(_ROUTES)
    values = []
    for _, _, ib, final, local in runs:
        for _, cb, expected in (final, *local):
            assert checker.verify_certificate(ib, cb) is None
            assert _REF.verify(ib, cb) == expected
        value = (final[2]["N"], final[2]["D"])
        expected = _EXPECTED_GLOBALS[gid]
        assert value[0] * expected[1] == expected[0] * value[1]
        values.append(value)
    assert values[0][0] * values[1][1] == values[1][0] * values[0][1]


def test_actual_local_origin_and_direct_h2_shapes(emissions):
    origins = Counter()
    shapes = Counter()
    for _, _, _, _, local in emissions:
        for origin, _, obj in local:
            origins[origin] += 1
            if origin == "H2":
                assert (obj["N"], obj["D"]) == (4, 2)
                counts = tuple(count for _, count in obj["y"])
                assert counts in ((2,), (1, 1))
                shapes[counts] += 1
    assert set(origins) == {"Baseline", "L0", "L1", "H0", "H1", "H2"}
    assert set(shapes) == {(2,), (1, 1)}
    assert sum(origins.values()) > 0


def test_distinct_tied_raw_pairs_are_valid_but_rescalings_are_not():
    first = _LITERALS["U17/TIE-SMALL"]
    second = _LITERALS["U17/TIE-LARGE"]
    assert first[0] == second[0]
    a, b = _REF.verify(*first[:2]), _REF.verify(*second[:2])
    assert a["N"] * b["D"] == b["N"] * a["D"]
    assert (a["N"], a["D"]) != (b["N"], b["D"])
    assert checker.verify_certificate(*first[:2]) is None
    assert checker.verify_certificate(*second[:2]) is None
    for name in ("PAIR-RESCALE-UP", "PAIR-REDUCE", "ZERO-NORMALIZE"):
        _, ib, cb, good, _ = _CASE_BY_ID["U18/" + name]
        assert good is False
        row = next(row for row in _TABLES["U18_WIRE_CASES"] if row[0] == name)
        original = _REF._parse(_LITERALS[row[1]][1])
        forged = _REF._parse(cb)
        assert original["N"] * forged["D"] == forged["N"] * original["D"]
        assert (original["N"], original["D"]) != (forged["N"], forged["D"])
        _invalid(checker.verify_certificate, ib, cb)


def test_no_hidden_solver_invocation_on_suboptimal_witness(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Hidden optimization or producer validation")

    ib, cb, _ = _LITERALS["U18/PAIR-ZERO"]
    for module, names in ((solver, ("solve", "_baseline", "_endpoint", "_evaluate")),
                          (producer, ("build_certificate", "serialize_certificate"))):
        for name in names:
            monkeypatch.setattr(module, name, forbidden)
    assert checker.verify_certificate(ib, cb) is None


def test_production_source_import_and_forbidden_operation_surface():
    tree = ast.parse(_CHECKER_PATH.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert all(alias.name == "json" for alias in node.names)
        if isinstance(node, ast.ImportFrom):
            assert node.level == 0
            assert node.module in {"json", "__future__"}
            if node.module == "__future__":
                assert [alias.name for alias in node.names] == ["annotations"]
        assert not isinstance(node, (ast.AsyncFunctionDef, ast.Await, ast.Global))
        assert not isinstance(node, ast.Div)
        if isinstance(node, ast.Call):
            name = (node.func.id if isinstance(node.func, ast.Name)
                    else node.func.attr if isinstance(node.func, ast.Attribute) else "")
            assert name not in {
                "open", "eval", "exec", "compile", "__import__", "input", "print", "exit",
                "set_int_max_str_digits", "setrecursionlimit", "settrace", "setprofile",
                "float", "Fraction", "Decimal", "gcd", "dumps", "dump", "load", "solve",
                "read", "read_bytes", "read_text", "write", "write_bytes", "write_text",
            }
        if isinstance(node, ast.ExceptHandler):
            assert node.type is not None
            names = {item.id for item in ast.walk(node.type) if isinstance(item, ast.Name)}
            assert not names & {
                "Exception", "BaseException", "ValueError", "MemoryError", "RecursionError",
            }
    assert _INDEPENDENT_WIRE_SOURCE not in _CHECKER_PATH.read_text()


_CHECKER_WORKER = r'''
import builtins
import hashlib
import importlib
import importlib.abc
import json
import sys
from pathlib import Path

payload = json.loads(sys.stdin.read())
root = Path(payload["root"]).resolve()
limit = sys.get_int_max_str_digits()
recursion = sys.getrecursionlimit()
assert limit == payload["limit"]
assert not any(name.split(".")[0] in {"exactfrac", "exactfrac_verify"} for name in sys.modules)
# The parent sanitizes PYTHONPATH; cwd is this independent-only export.
sys.path.insert(0, str(root))

class BlockProjects(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "exactfrac" or fullname.startswith("exactfrac."):
            raise ImportError("Producer import forbidden")
''' '        if fullname.split(".")[0] in {"tests", "fixture_support", "independ' \
    'ent_wire", "unit18_support"}:' r'''
            raise ImportError("Private/test import forbidden")
        if fullname.startswith("exactfrac_verify.") and fullname != "exactfrac_verify.check":
            raise ImportError("Unrelated independent helper forbidden")
        return None

sys.meta_path.insert(0, BlockProjects())
module = importlib.import_module("exactfrac_verify.check")
assert Path(module.__file__).resolve() == root / "exactfrac_verify/check.py"
assert hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == payload["source_sha256"]
assert type(module.__all__) is tuple and module.__all__ == ("verify_certificate",)
origins = {}
for name, value in sorted(sys.modules.items()):
    if name == "exactfrac" or name.startswith("exactfrac."):
        raise AssertionError("Producer loaded")
    if name == "exactfrac_verify" or name.startswith("exactfrac_verify."):
        path = Path(value.__file__).resolve()
        assert path.is_relative_to(root)
        origins[name] = str(path.relative_to(root))
assert set(origins) == {"exactfrac_verify", "exactfrac_verify.check"}

# Import loading has completed. Verification itself must not perform external I/O.
def audit(event, args):
    if event in {"open", "compile", "exec", "os.system", "os.chdir", "os.listdir", "os.scandir"}:
        raise AssertionError("Forbidden runtime operation: " + event)
    if event.startswith(("socket.", "subprocess.", "os.remove", "os.rename", "os.mkdir")):
        raise AssertionError("Forbidden runtime operation: " + event)

sys.addaudithook(audit)

def retained(value, inputs, seen):
    if any(value is raw for raw in inputs):
        return True
    identity = id(value)
    if identity in seen:
        return False
    seen.add(identity)
    if type(value) is dict:
        return any(retained(x, inputs, seen) for pair in value.items() for x in pair)
    if type(value) in (list, tuple, set, frozenset):
        return any(retained(x, inputs, seen) for x in value)
    if getattr(type(value), "__module__", "") == module.__name__:
        if hasattr(value, "__dict__") and retained(vars(value), inputs, seen):
            return True
        for name in getattr(type(value), "__slots__", ()):
            if hasattr(value, name) and retained(getattr(value, name), inputs, seen):
                return True
    return False

accepted = rejected = 0
for key, ih, ch, good in payload["pairs"]:
    ib, cb = bytes.fromhex(ih), bytes.fromhex(ch)
    for repeat in range(2):
        try:
            result = module.verify_certificate(ib, cb)
        except ValueError as error:
            assert type(error) is ValueError and not good, key
            if repeat == 0:
                rejected += 1
        else:
            assert good and result is None, key
            if repeat == 0:
                accepted += 1
        assert ib.hex() == ih and cb.hex() == ch
        assert not retained(vars(module), (ib, cb), set()), "Retained caller input: " + key
assert sys.get_int_max_str_digits() == limit
assert sys.getrecursionlimit() == recursion
assert not any(name == "exactfrac" or name.startswith("exactfrac.") for name in sys.modules)
print(json.dumps({"accepted": accepted, "rejected": rejected, "limit": limit,
                  "settings_unchanged": True, "project_modules": origins,
                  "producer_imports": [], "input_retained": False}, sort_keys=True))
'''

_REFERENCE_WORKER = r'''
import builtins
import importlib.abc
import json
import sys

payload = json.loads(sys.stdin.read())
limit = sys.get_int_max_str_digits()
assert limit == payload["limit"]

class BlockProjects(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in {"exactfrac", "exactfrac_verify", "tests"}:
            raise ImportError("No project imports in independent byte reference")
        return None

sys.meta_path.insert(0, BlockProjects())
space = {"__name__": "_separate_unit18_byte_reference"}
exec(compile(payload["source"], "<separate-unit18-reference>", "exec"), space)
accepted = rejected = 0
for key, ih, ch, good in payload["pairs"]:
    try:
        result = space["verify"](bytes.fromhex(ih), bytes.fromhex(ch))
    except ValueError as error:
        assert type(error) is ValueError and not good, key
        rejected += 1
    else:
        assert good and type(result) is dict, key
        accepted += 1
assert sys.get_int_max_str_digits() == limit
''' 'assert not any(name.split(".")[0] in {"exactfrac", "exactfrac_v' \
    'erify", "tests"} for name in sys.modules)' r'''
print(json.dumps({"accepted": accepted, "rejected": rejected, "limit": limit,
                  "project_imports": [], "settings_unchanged": True}, sort_keys=True))
'''


def _fresh(worker, payload, limit, seed, cwd):
    env = {key: value for key, value in os.environ.items()
           if key not in {"PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP", "PYTHONINSPECT"}}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONNOUSERSITE="1", PYTHONHASHSEED=seed)
    completed = subprocess.run(
        [sys.executable, "-B", "-s", "-X", "int_max_str_digits=" + str(limit), "-c", worker],
        input=json.dumps({**payload, "limit": limit}, ensure_ascii=True).encode(),
        capture_output=True, cwd=cwd, env=env, check=False, timeout=180,
    )
    assert completed.returncode == 0, completed.stderr.decode("utf-8", "replace")
    return json.loads(completed.stdout)


def _wire_payload():
    return [(key, ib.hex(), cb.hex(), good) for key, ib, cb, good, _ in _CASES]


@pytest.mark.parametrize(
    "limit,seed", [(limit, seed) for seed in ("1", "73") for limit in (4300, 640)]
)
def test_separate_reference_large_integer_semantics(limit, seed, tmp_path):
    result = _fresh(
        _REFERENCE_WORKER, {"source": _INDEPENDENT_WIRE_SOURCE, "pairs": _wire_payload()},
                    limit, seed, tmp_path)
    assert result == {"accepted": 64, "rejected": 455, "limit": limit,
                      "project_imports": [], "settings_unchanged": True}


@pytest.mark.parametrize(
    "limit,seed", [(limit, seed) for seed in ("1", "73") for limit in (4300, 640)]
)
def test_checker_only_export_large_integer_rejection_and_runtime_isolation(limit, seed, tmp_path):
    package = tmp_path / "exactfrac_verify"
    package.mkdir()
    (package / "__init__.py").write_bytes(b"")
    source = _CHECKER_PATH.read_bytes()
    (package / "check.py").write_bytes(source)
    before = {str(path.relative_to(tmp_path)): path.read_bytes()
              for path in sorted(tmp_path.rglob("*")) if path.is_file()}
    result = _fresh(_CHECKER_WORKER, {"root": str(tmp_path), "source_sha256": _sha(source),
                                    "pairs": _wire_payload()}, limit, seed, tmp_path)
    assert result == {"accepted": 64, "rejected": 455, "limit": limit,
                      "settings_unchanged": True, "producer_imports": [], "input_retained": False,
                      "project_modules": {"exactfrac_verify": "exactfrac_verify/__init__.py",
                                          "exactfrac_verify.check": "exactfrac_verify/check.py"}}
    assert {str(path.relative_to(tmp_path)): path.read_bytes()
            for path in sorted(tmp_path.rglob("*")) if path.is_file()} == before


def test_every_real_emission_is_accepted_with_only_checker_files_available(emissions, tmp_path):
    package = tmp_path / "exactfrac_verify"
    package.mkdir()
    (package / "__init__.py").write_bytes(b"")
    source = _CHECKER_PATH.read_bytes()
    (package / "check.py").write_bytes(source)
    pairs = []
    for gid, route, ib, final, local in emissions:
        for index, (_, cb, _) in enumerate((final, *local)):
            pairs.append((gid + "/" + route + "/" + str(index), ib.hex(), cb.hex(), True))
    assert len(pairs) > 800
    result = _fresh(_CHECKER_WORKER, {"root": str(tmp_path), "source_sha256": _sha(source),
                                    "pairs": pairs}, 4300, "73", tmp_path)
    assert result["accepted"] == len(pairs)
    assert result["rejected"] == 0
    assert result["producer_imports"] == []
    assert result["input_retained"] is False
    assert (package / "check.py").read_bytes() == source


def test_old_prefix_guard_remains_length_checked_and_append_tolerant():
    test = (_ROOT / "tests/test_certificate.py").read_bytes()
    guard = (
        b"    catalogue_bytes = _CATALOGUE.read_bytes()\n"
        b"    assert len(catalogue_bytes) >= 3_212_040\n"
        b"    assert _sha(catalogue_bytes[:3_212_040]) == _CATALOGUE_SHA\n"
    )
    assert test.count(guard) == 1
    original = _CATALOGUE.read_bytes()[:3_212_040]
    assert _sha(original) == "04ef6a4b38463aecb0d86731d1873aadb4acb8bc8a8593e0ea82b4325e56e7ac"
    code = compile(
        "\n".join(line[4:] for line in guard.decode().splitlines()), "<fixed-prefix-guard>", "exec"
    )
    cases = [original, original + b"authorized future append", b"", original[:-1]]
    for index in (0, len(original) // 2, len(original) - 1):
        cases.append(original[:index] + bytes([original[index] ^ 1]) + original[index + 1:])
    for index, raw in enumerate(cases):
        space = {"_CATALOGUE": types.SimpleNamespace(read_bytes=lambda data=raw: data),
                 "_sha": _sha, "_CATALOGUE_SHA": _SUPPORT.PREFIX_SHA}
        if index < 2:
            exec(code, space)
        else:
            with pytest.raises(AssertionError):
                exec(code, space)


def test_metadata_changes_can_preserve_attainment_without_digest_binding():
    ib, cb, _ = _LITERALS["U18/PAIR-FULL"]
    graph = _REF.parse_instance(ib)
    graph["labels"] = ["different-left", "different-right"]
    changed = _FIX.encode(graph)
    assert changed != ib
    assert _REF.verify(changed, cb) == _REF.verify(ib, cb)
    assert checker.verify_certificate(changed, cb) is None
    # A different active instance can also admit exactly the same local zero pair.
    ib, cb, _ = _LITERALS["U18/PAIR-ZERO"]
    graph = _REF.parse_instance(ib)
    graph["edges"][0][2] += 1
    changed = _FIX.encode(graph)
    assert changed != ib
    assert _REF.verify(changed, cb) == _REF.verify(ib, cb)
    assert checker.verify_certificate(changed, cb) is None
