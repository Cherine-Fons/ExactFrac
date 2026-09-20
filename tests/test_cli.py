"""Unit 19 consuming tests for the adopted CLI composition contract.

Expected bytes, token outcomes and mathematical identities come from the closed
catalogue, never from the CLI. Private embedded references are test transport and
independent validators, not runtime dependencies. No production CLI is supplied.
"""

from __future__ import annotations

import ast
import builtins
import copy
import gc
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
import exactfrac.cli as _cli

# isort: split
import exactfrac.certificate as _certificate
import exactfrac.instance as _instance
import exactfrac.solve as _solver
import exactfrac_verify.check as _checker
from exactfrac.witness import ExactValue, Witness

_ROOT = Path(__file__).resolve().parents[1]
_CATALOGUE = _ROOT / "docs/ORACLE_CATALOG.md"
_CLI_PATH = _ROOT / "exactfrac/cli.py"
_ROUTES = ("Standard", "Accelerated")


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


# BYTE-IDENTICAL_EMBEDDED_REFERENCE_SOURCES

_REFERENCE_SOURCES = {
    'independent_wire': (
        '"""Phase C test-only byte-pair oracle; not Unit 18 production cod'
        'e.\n\nNo ExactFrac imports, no production helpers, no file I/O and '
        'no expected answers.\nThe public-to-this-private-module verificati'
        'on function accepts only two bytes objects.\nA lexical certificate'
        ' grammar is checked without re-encoding the decoded object.\n"""\ni'
        "mport json\nimport re\n\n_NUM = rb'(?:0|[1-9][0-9]*)'\n_POS = rb'(?:["
        "1-9][0-9]*)'\n_U = rb'\\[' + _NUM + rb'(?:,' + _NUM + rb')*\\]'\n_PAI"
        "R = rb'\\[' + _NUM + rb',' + _POS + rb'\\]'\n_Y = rb'\\[(?:' + _PAIR "
        '+ rb\'(?:,\' + _PAIR + rb\')*)?\\]\'\n_EMPTY = rb\'\\{"format":"exactfrac'
        '-certificate/1","empty":true,"N":\' + _NUM + rb\',"D":\' + _POS + rb'
        '\'\\}\\n\'\n_NONEMPTY = (rb\'\\{"format":"exactfrac-certificate/1","empt'
        'y":false,"N":\' + _NUM\n            + rb\',"D":\' + _POS + rb\',"U":\' '
        '+ _U + rb\',"y":\' + _Y + rb\'\\}\\n\')\n_CERTIFICATE = re.compile(rb\'(?'
        ":' + _EMPTY + rb'|' + _NONEMPTY + rb')')\n_INTEGER = re.compile(r'"
        "(?:0|-?[1-9][0-9]*)')\n\n\ndef _require(condition, reason):\n    if n"
        'ot condition:\n        raise ValueError(reason)\n\n\ndef _decimal(tok'
        "en):\n    _require(_INTEGER.fullmatch(token) is not None, 'noncano"
        "nical integer token')\n    negative = token.startswith('-')\n    di"
        'gits = token[1:] if negative else token\n    value = 0\n    # No fu'
        'll-token int conversion; each conversion is at most seven digits.'
        '\n    for position in range(0, len(digits), 7):\n        chunk = di'
        'gits[position:position + 7]\n        value = value * (10 ** len(ch'
        'unk)) + int(chunk)\n    return -value if negative else value\n\n\ndef'
        " _no_noninteger(_token):\n    raise ValueError('noninteger number "
        "token')\n\n\ndef _object(pairs):\n    result = {}\n    for key, value "
        "in pairs:\n        _require(key not in result, 'duplicate decoded "
        "key')\n        result[key] = value\n    return result\n\n\ndef _parse("
        "raw):\n    _require(type(raw) is bytes, 'serialized input must be "
        "exact bytes')\n    _require(not raw.startswith(b'\\xef\\xbb\\xbf'), '"
        "UTF-8 BOM forbidden')\n    try:\n        text = raw.decode('utf-8')"
        "\n    except UnicodeDecodeError as exc:\n        raise ValueError('"
        "invalid UTF-8') from exc\n    try:\n        return json.loads(text,"
        ' object_pairs_hook=_object, parse_int=_decimal,\n                 '
        '         parse_float=_no_noninteger, parse_constant=_no_nonintege'
        'r)\n    except json.JSONDecodeError as exc:\n        raise ValueErr'
        "or('invalid JSON document') from exc\n\n\ndef parse_instance(raw):\n "
        '   """Decode and validate canonical graph data; do not sort or ag'
        'gregate."""\n    data = _parse(raw)\n    _require(type(data) is dic'
        "t, 'instance must be object')\n    keys = set(data)\n    _require(k"
        "eys in ({'format', 'n', 'edges', 'f'},\n                      {'fo"
        "rmat', 'n', 'edges', 'f', 'labels'}), 'instance fields')\n    _req"
        "uire(type(data['format']) is str and data['format'] == 'exactfrac"
        "-instance/1',\n             'instance format')\n    n = data['n']\n "
        "   _require(type(n) is int and n >= 1, 'positive integer n')\n    "
        "f = data['f']\n    _require(type(f) is list and len(f) == n, 'f le"
        "ngth/type')\n    _require(all(type(x) is int and x >= 1 for x in f"
        "), 'positive integer f')\n    if 'labels' in data:\n        labels "
        "= data['labels']\n        _require(type(labels) is list and len(la"
        "bels) == n, 'labels length/type')\n        _require(all(type(x) in"
        " (int, str) for x in labels), 'label exact types')\n        _requi"
        "re(len(set(labels)) == len(labels), 'duplicate labels')\n    edges"
        " = data['edges']\n    _require(type(edges) is list and len(edges) "
        "> 0, 'nonempty support')\n    degrees = [0] * n\n    previous = Non"
        'e\n    for edge in edges:\n        _require(type(edge) is list and '
        "len(edge) == 3, 'edge shape')\n        u, v, q = edge\n        _req"
        "uire(all(type(x) is int for x in edge), 'integer edge fields')\n  "
        "      _require(0 <= u < v < n and q >= 1, 'edge range/orientation"
        "/multiplicity')\n        _require(previous is None or previous < ("
        "u, v), 'strict canonical edge order')\n        previous = (u, v)\n "
        '       degrees[u] += q\n        degrees[v] += q\n    _require(all(c'
        "ap <= degree for cap, degree in zip(f, degrees)), 'active conditi"
        "on')\n    return data\n\n\ndef verify(instance_bytes, certificate_byt"
        'es):\n    """Independently return a decoded certificate iff admiss'
        'ible/raw-attaining or Empty.\n\n    Validation of the complete inst'
        'ance precedes parsing the certificate and hence\n    precedes ever'
        'y interpretation of an edge reference. No optimality is asserted.'
        '\n    """\n    instance = parse_instance(instance_bytes)\n    _requi'
        "re(type(certificate_bytes) is bytes, 'certificate must be exact b"
        "ytes')\n    _require(_CERTIFICATE.fullmatch(certificate_bytes) is "
        "not None, 'certificate wire grammar')\n    cert = _parse(certifica"
        'te_bytes)\n    # Grammar checks precede object creation; duplicate'
        '/escaped/reordered keys cannot match.\n    _require(type(cert) is '
        "dict, 'certificate object')\n    _require(type(cert['empty']) is b"
        "ool and type(cert['N']) is int and type(cert['D']) is int,\n      "
        "       'certificate field types')\n    _require(cert['N'] >= 0 and"
        " cert['D'] > 0, 'certificate signs')\n    if cert['empty']:\n      "
        "  _require(sum(edge[2] for edge in instance['edges']) == 1, 'fals"
        "e Empty')\n        _require((cert['N'], cert['D']) == (0, 1), 'lit"
        "eral Empty pair')\n        return cert\n    U = cert['U']\n    _requ"
        "ire(type(U) is list and bool(U), 'nonempty U')\n    _require(all(t"
        "ype(v) is int and 0 <= v < instance['n'] for v in U), 'vertex ran"
        "ge/type')\n    _require(all(a < b for a, b in zip(U, U[1:])), 'str"
        "ict U order')\n    shore = set(U)\n    y = cert['y']\n    _require(t"
        "ype(y) is list, 'sparse list')\n    previous = -1\n    selected = 0"
        '\n    for entry in y:\n        _require(type(entry) is list and len'
        "(entry) == 2, 'sparse pair shape')\n        ref, count = entry\n   "
        "     _require(type(ref) is int and type(count) is int, 'sparse ex"
        "act integers')\n        _require(previous < ref < len(instance['ed"
        "ges']), 'sparse reference order/range')\n        previous = ref\n  "
        "      u, v, q = instance['edges'][ref]\n        _require(0 < count"
        " <= q, 'sparse positive bounded count')\n        _require((u in sh"
        "ore) != (v in shore), 'sparse crossing constraint')\n        selec"
        "ted += count\n    s = sum(instance['f'][v] for v in U)\n    e = sum"
        "(q for u, v, q in instance['edges'] if u in shore and v in shore)"
        "\n    _require((s + selected) % 2 == 1, 'odd admissibility')\n    _"
        "require(s + selected >= 3, 'minimum admissibility')\n    _require("
        "cert['N'] == 2 * (e + selected), 'literal numerator')\n    _requir"
        "e(cert['D'] == s + selected - 1, 'literal denominator')\n    retur"
        'n cert\n'
    ),
    'fixture_support': (
        '"""Private Phase C catalogue/derivation utilities, never producti'
        'on verifier helpers."""\nimport ast\nimport hashlib\nimport itertool'
        "s\nimport json\nfrom pathlib import Path\n\nSYMBOLS = {'T': 10**4800,"
        " 'Tm1':10**4800-1, 'Tp1':10**4800+1,\n           'twoT':2*10**4800"
        ", 'twoTm2':2*10**4800-2, 'minusT':-(10**4800)}\n\ndef number(x):\n  "
        "  if type(x) is tuple and len(x)==2 and x[0]=='sym':\n        retu"
        'rn SYMBOLS[x[1]]\n    if type(x) is not int:\n        raise ValueEr'
        "ror('not an integer/symbol fixture')\n    return x\n\ndef compact_nu"
        'mber(x):\n    for name,value in SYMBOLS.items():\n        if x==val'
        "ue:return ('sym',name)\n    return x\n\ndef read_tables(path, prefix"
        "es=('U15_INPUTS','U16_INPUTS','U15_GLOBAL','U15_BASELINES',\n     "
        "                          'U15_H2','U15_SHORES','U17_')):\n    tab"
        'les={}; current=None; header=False\n    for line in Path(path).rea'
        "d_text(encoding='utf-8').splitlines():\n        if line.startswith"
        "('### Fixture table: '):\n            name=line.split(': ',1)[1]\n "
        '           current=name if any(name.startswith(p) for p in prefix'
        'es) else None\n            if current:\n                if name in '
        "tables:raise ValueError('duplicate table '+name)\n                "
        'tables[name]=[];header=True\n        elif current and line.startsw'
        "ith('| '):\n            cells=[v.strip() for v in line[1:-1].split"
        "('|')]\n            if header:header=False\n            elif not al"
        "l(v=='---' for v in cells):\n                if not all(v.startswi"
        "th('`') and v.endswith('`') for v in cells):\n                    "
        "raise ValueError('nonliteral fixture cell')\n                table"
        's[current].append(tuple(ast.literal_eval(v[1:-1]) for v in cells)'
        ')\n        elif current and line.strip():current=None\n    return t'
        'ables\n\ndef digits(value):\n    negative=value<0; value=abs(value)\n'
        "    if value==0:return b'0'\n    pieces=[]\n    while value:\n      "
        '  value,remainder=divmod(value,100000)\n        pieces.append(rema'
        "inder)\n    output=str(pieces.pop()).encode('ascii')\n    output+=b"
        "''.join(('%05d'%v).encode('ascii') for v in reversed(pieces))\n   "
        " return (b'-' if negative else b'')+output\n\ndef encode(value):\n  "
        '  """Untrusted test transport encoder; NOT the expected-byte reci'
        'pe nor verifier."""\n    if value is None:return b\'null\'\n    if ty'
        "pe(value) is bool:return b'true' if value else b'false'\n    if ty"
        'pe(value) is int:return digits(value)\n    if type(value) is str:r'
        "eturn json.dumps(value,ensure_ascii=True).encode('ascii')\n    if "
        "type(value) in (list,tuple):return b'['+b','.join(encode(x) for x"
        " in value)+b']'\n    if type(value) is dict:return b'{'+b','.join("
        "encode(k)+b':'+encode(v) for k,v in value.items())+b'}'\n    raise"
        " ValueError('transport type')\n\ndef fingerprint(rows):\n    return "
        "hashlib.sha256(b''.join(encode(row)+b'\\n' for row in rows)).hexdi"
        'gest()\n\ndef registry(tables):\n    records=[]\n    for key,kind,n,e'
        "dges,f,labels in tables['U15_INPUTS']:\n        records.append(('U"
        "15_INPUTS/'+key,{'format':'exactfrac-instance/1','n':n,\n         "
        "               'edges':[list(e) for e in edges],'f':list(f),\n    "
        "                    **({} if labels is None else {'labels':list(l"
        "abels)})}))\n    for key,n,edges,f,labels in tables['U16_INPUTS']:"
        "\n        records.append(('U16_INPUTS/'+key,{'format':'exactfrac-i"
        "nstance/1','n':n,\n                        'edges':[list(e) for e "
        "in edges],'f':list(f),\n                        **({} if labels is"
        " None else {'labels':list(labels)})}))\n    for key,n,edges,f,labe"
        "ls in tables.get('U17_INPUTS',[]):\n        lab=None if labels is "
        'None else [number(x) if type(x) is tuple else x for x in labels]\n'
        "        records.append(('U17_INPUTS/'+key,{'format':'exactfrac-in"
        "stance/1','n':n,\n                       'edges':[[u,v,number(q)] "
        "for u,v,q in edges],'f':[number(x) for x in f],\n                 "
        "      **({} if lab is None else {'labels':lab})}))\n    if len({k "
        "for k,_ in records})!=len(records):raise ValueError('duplicate re"
        "gistry identity')\n    return records\n\ndef recipe(parts):\n    resu"
        'lt=[]\n    for part in parts:\n        if type(part) is str:result.'
        "append(part.encode('ascii'))\n        elif type(part) is tuple and"
        " len(part)==3 and part[0]=='repeat':\n            char,count=part["
        '1:]\n            if type(char) is not str or len(char)!=1 or type('
        "count) is not int or count<0:\n                raise ValueError('b"
        "ad repeat')\n            result.append(char.encode('ascii')*count)"
        "\n        else:raise ValueError('bad byte recipe')\n    return b''."
        "join(result)\n\ndef witness_certificate(U,y,N,D):\n    obj={'format'"
        ":'exactfrac-certificate/1','empty':U is None,'N':N,'D':D}\n    if "
        'U is not None:obj.update(U=list(U),y=[list(x) for x in y])\n    re'
        'turn obj\n\ndef raw_value(graph,U,y):\n    """Direct independent pri'
        'mitive evaluation for derivation, not byte validation."""\n    s=s'
        "um(graph['f'][v] for v in U)\n    Y=sum(count for _,count in y)\n  "
        "  e=sum(q for u,v,q in graph['edges'] if u in U and v in U)\n    b"
        "=sum(q for u,v,q in graph['edges'] if (u in U)!=(v in U))\n    ret"
        'urn 2*(e+Y),s+Y-1,(s,e,b,Y)\n\ndef realize(graph,U,Y):\n    y=[]\n   '
        " for ref,(u,v,q) in enumerate(graph['edges']):\n        if (u in U"
        ')!=(v in U):\n            take=min(q,Y);Y-=take\n            if tak'
        "e:y.append((ref,take))\n    if Y:raise ValueError('unrealizable to"
        "tal')\n    return tuple(y)\n\ndef global_reference(graph,mode='endpo"
        'ints\'):\n    """Exhaustive finite private oracle; no production br'
        'anch algorithm is reproduced.\n\n    Full-vector/scalar enumeration'
        ' is used only on declared finite small cases.\n    Endpoint mode s'
        'cans 2^n-1 shores but never scans q, f or Q copies.\n    """\n    b'
        "est=None\n    for mask in range(1,1<<graph['n']):\n        U=tuple("
        "v for v in range(graph['n']) if mask & (1<<v))\n        s=sum(grap"
        "h['f'][v] for v in U)\n        e=sum(q for u,v,q in graph['edges']"
        ' if u in U and v in U)\n        boundary=[(ref,q) for ref,(u,v,q) '
        "in enumerate(graph['edges']) if (u in U)!=(v in U)]\n        b=sum"
        "(q for _,q in boundary)\n        if mode=='vectors':\n            i"
        'tems=((sum(counts),tuple((ref,t) for (ref,_),t in zip(boundary,co'
        'unts) if t))\n                   for counts in itertools.product(*'
        '(range(q+1) for _,q in boundary)))\n        else:\n            low='
        '2 if s==1 else (1 if s%2==0 else 0)\n            high=b-((s+b+1)%2'
        ")\n            totals=range(b+1) if mode=='scalars' else ((low,) i"
        'f high==low else (low,high))\n            items=((t,None) for t in'
        ' totals if 0<=t<=b)\n        for Y,y in items:\n            if (s+Y'
        ')%2!=1 or s+Y<3:continue\n            N,D=2*(e+Y),s+Y-1\n          '
        '  if best is None or N*best[1]>best[0]*D:\n                best=(N'
        ',D,U,realize(graph,U,Y) if y is None else y)\n    return (0,1,None'
        ',None) if best is None else best\n\ndef same_value(a,b):return a[0]'
        '*b[1]==b[0]*a[1]\n\ndef small_for_exhaustion(graph):return max(q fo'
        "r _,_,q in graph['edges'])<=6\n"
    ),
    'fixture_mutations': (
        '"""Execute catalogue-declared wire adversaries; no production int'
        'eraction."""\nimport json\nfrom fixture_support import encode\nfrom '
        'independent_wire import _parse\n\ndef mutate(raw,operations):\n    f'
        'or operation in operations:\n        op=operation[0]\n        if op'
        " in ('set','delete'):\n            document=_parse(raw)\n          "
        '  target=document\n            for part in operation[1][:-1]:targe'
        "t=target[part]\n            if op=='set':target[operation[1][-1]]="
        'operation[2]\n            else:del target[operation[1][-1]]\n      '
        "      raw=encode(document)+(b'\\n' if raw.endswith(b'\\n') else b''"
        ")\n        elif op=='replace':\n            a,b=operation[1].encode"
        "('utf-8'),operation[2].encode('utf-8')\n            if raw.count(a"
        ")!=1:raise ValueError('replacement not unique: '+operation[1])\n  "
        "          raw=raw.replace(a,b)\n        elif op=='prefix':raw=oper"
        "ation[1].encode('utf-8')+raw\n        elif op=='prefix_hex':raw=by"
        "tes.fromhex(operation[1])+raw\n        elif op=='suffix':raw+=oper"
        "ation[1].encode('utf-8')\n        elif op=='strip_final_lf':\n     "
        "       if not raw.endswith(b'\\n'):raise ValueError('no LF')\n     "
        "       raw=raw[:-1]\n        elif op=='reverse_keys':\n            "
        "d=_parse(raw);raw=encode(dict(reversed(list(d.items()))))+(b'\\n' "
        "if raw.endswith(b'\\n') else b'')\n        elif op=='pretty':raw=js"
        "on.dumps(_parse(raw),ensure_ascii=True,indent=2).encode('ascii')+"
        "b'\\n'\n        elif op=='utf8_strings':raw=json.dumps(_parse(raw),"
        "ensure_ascii=False,separators=(',',':')).encode('utf-8')\n        "
        'elif op==\'quote_field\':\n            name=operation[1];token=b\'"\'+'
        'name.encode()+b\'":\';start=raw.index(token)+len(token)\n           '
        ' end=start\n            while end<len(raw) and 48<=raw[end]<=57:en'
        'd+=1\n            raw=raw[:start]+b\'"\'+raw[start:end]+b\'"\'+raw[end'
        ":]\n        else:raise ValueError('unknown mutation operation')\n  "
        '  return raw\n'
    ),
    'unit18_support': (
        '"""Private Unit 18 fixture assembly. No checker code; no producti'
        'on imports.\n\nTables, byte recipes and independent mathematical re'
        'ferences are the authority.\nThis module is a test transport, neve'
        'r the expected verdict\'s derivation.\n"""\nfrom pathlib import Path'
        '\nimport hashlib\nfrom fixture_support import (read_tables, registr'
        'y, encode, number, recipe, fingerprint)\nfrom fixture_mutations im'
        "port mutate\n\nPREFIX_LENGTH = 3_212_040\nPREFIX_SHA = '04ef6a4b3846"
        "3aecb0d86731d1873aadb4acb8bc8a8593e0ea82b4325e56e7ac'\nOLD_TEST_SH"
        "A = 'c70f7120fe10d07668fc37624843cc77a02ef58244fbda432d0459112304"
        "2724'\nOLD_GUARD = b'    assert _sha(_CATALOGUE.read_bytes()) == _"
        "CATALOGUE_SHA\\n'\nNEW_GUARD = (b'    catalogue_bytes = _CATALOGUE."
        "read_bytes()\\n'\n             b'    assert len(catalogue_bytes) >="
        " 3_212_040\\n'\n             b'    assert _sha(catalogue_bytes[:3_2"
        "12_040]) == _CATALOGUE_SHA\\n')\nABSENCE = b'    assert not (_ROOT "
        '/ "exactfrac_verify/check.py").exists()\\n\'\n\ndef tables_at(path):\n'
        "    return read_tables(path, ('U15_INPUTS','U16_INPUTS','U15_GLOB"
        "AL','U15_BASELINES',\n                             'U15_H2','U15_S"
        "HORES','U17_','U18_'))\n\ndef all_graphs(tables):\n    answer = regi"
        "stry(tables)\n    for key,n,edges,f,labels in tables['U18_INPUTS']"
        ":\n        answer.append(('U18_INPUTS/'+key, {'format':'exactfrac-"
        "instance/1','n':n,\n              'edges':[[u,v,number(q)] for u,v"
        ",q in edges], 'f':[number(x) for x in f],\n              **({} if "
        "labels is None else {'labels':list(labels)})}))\n    if len({k for"
        " k,g in answer}) != len(answer):\n        raise AssertionError('Du"
        "plicate qualified registry identity')\n    return answer\n\ndef lite"
        'rals(tables):\n    graphs = dict(all_graphs(tables)); out = {}\n   '
        " for table,prefix in (('U17_BYTES','U17/'),('U18_LITERALS','U18/'"
        ')):\n        for row in tables[table]:\n            key,gid,kind,U,'
        'y,N,D,parts,size,digest = row\n            wire = recipe(parts)\n  '
        '          if len(wire)!=size or hashlib.sha256(wire).hexdigest()!'
        "=digest:\n                raise AssertionError('Literal identity '"
        '+key)\n            out[prefix+key] = (encode(graphs[gid]),wire,row'
        ')\n    return out\n\ndef byte_edit(raw, operations):\n    for op in o'
        "perations:\n        if op[0]=='raw_hex': raw = bytes.fromhex(op[1]"
        ")\n        elif op[0]=='truncate': raw = raw[:op[1]]\n        elif "
        "op[0]=='replace_hex':\n            old,new = bytes.fromhex(op[1]),"
        'bytes.fromhex(op[2])\n            if raw.count(old)!=1: raise Asse'
        "rtionError('Hex replacement not unique')\n            raw=raw.repl"
        "ace(old,new)\n        elif op[0]=='encoding':\n            raw=raw."
        "decode('utf-8').encode(op[1])\n        else: raw = mutate(raw,(op,"
        '))\n    return raw\n\ndef wire_cases(tables):\n    fixed=literals(tab'
        'les); cases=[]\n    for key,(ib,cb,row) in fixed.items():\n        '
        "cases.append((key,ib,cb,True,'literal'))\n    for name,good in (('"
        "U17_WIRE_REJECT',False),('U17_WIRE_ACCEPT',True)):\n        for ro"
        'w in tables[name]:\n            if good:key,bid,stream,ops,size,di'
        'gest=row\n            else:key,bid,stream,ops,reason,equal,size,di'
        "gest=row\n            ib,cb,_=fixed['U17/'+bid]; changed=byte_edit"
        "(ib if stream=='instance' else cb,ops)\n            if len(changed"
        ')!=size or hashlib.sha256(changed).hexdigest()!=digest:\n         '
        "       raise AssertionError('Inherited byte row '+key)\n          "
        "  cases.append(('U17/'+key,changed if stream=='instance' else ib,"
        "\n                          changed if stream=='certificate' else "
        "cb,good,'inherited'))\n    for key,bid,stream,ops,good,reason,size"
        ",digest in tables['U18_WIRE_CASES']:\n        ib,cb,_=fixed[bid]; "
        "changed=byte_edit(ib if stream=='instance' else cb,ops)\n        i"
        'f len(changed)!=size or hashlib.sha256(changed).hexdigest()!=dige'
        "st:\n            raise AssertionError('Unit18 byte row '+key)\n    "
        "    cases.append(('U18/'+key,changed if stream=='instance' else i"
        "b,\n                      changed if stream=='certificate' else cb"
        ',good,reason))\n    if len({c[0] for c in cases})!=len(cases):rais'
        "e AssertionError('Duplicate wire identity')\n    return cases\n\ndef"
        ' guarded_prefix(raw):\n    if len(raw)<PREFIX_LENGTH:raise ValueEr'
        "ror('Catalogue shorter than protected prefix')\n    if hashlib.sha"
        '256(raw[:PREFIX_LENGTH]).hexdigest()!=PREFIX_SHA:\n        raise V'
        "alueError('Historical catalogue bytes changed')\n\ndef exact_test_t"
        'ransition(old,new):\n    if hashlib.sha256(old).hexdigest()!=OLD_T'
        "EST_SHA:raise AssertionError('Original Unit17 test identity')\n   "
        ' if old.count(OLD_GUARD)!=1 or old.count(ABSENCE)!=2:raise Assert'
        "ionError('Original guard/absence census')\n    if new != old.repla"
        "ce(OLD_GUARD,NEW_GUARD,1):raise AssertionError('Unauthorized test"
        " byte change')\n    if new.count(ABSENCE)!=2:raise AssertionError("
        "'Phase D absence line retired early')\n    return True\n"
    ),
    'unit19_support': (
        '"""Private Phase C table interpretation, not a production CLI or '
        'public parser.\n\nExpected rows are hand-derived from adopted DESIG'
        'N 4.16. This module independently\nchecks consistency; it performs'
        ' no command I/O and no solver/checker imports.\n"""\nfrom pathlib i'
        'mport Path\nimport hashlib\nfrom fixture_support import read_tables'
        ", recipe\n\nPREFIXES = ((3212040, '04ef6a4b38463aecb0d86731d1873aad"
        "b4acb8bc8a8593e0ea82b4325e56e7ac'),\n            (3312641, '05255f"
        "65148c007278a38df664df5e6ff02db868d63fdafe7d9a016861952840'))\n\n\nd"
        'ef require(condition, why):\n    if not condition:\n        raise A'
        'ssertionError(why)\n\n\ndef tables_at(path):\n    return read_tables('
        "path, ('U15_INPUTS','U16_INPUTS','U15_GLOBAL','U15_BASELINES',\n  "
        "                           'U15_H2','U15_SHORES','U17_','U18_','U"
        "19_'))\n\n\ndef bytes_recipe(parts):\n    result = []\n    for part in"
        ' parts:\n        if type(part) is tuple and len(part) == 2 and par'
        "t[0] == 'hex':\n            result.append(bytes.fromhex(part[1]))\n"
        '        else:\n            result.append(recipe((part,)))\n    retu'
        "rn b''.join(result)\n\n\ndef protect(raw):\n    for length, digest in"
        " PREFIXES:\n        require(len(raw) >= length, 'Truncated histori"
        "cal catalogue')\n        require(hashlib.sha256(raw[:length]).hexd"
        "igest() == digest, 'Changed historical catalogue')\n\n\ndef grammar("
        'tokens):\n    """Declarative token-spec checker: returns only (kin'
        'd, selection, operands).\n\n    No stream handling, exception trans'
        'lation, main, or production dependency.\n    The table remains the'
        ' expected answer rather than the classifier\'s output.\n    """\n   '
        " help_forms = {('-h',): 'ROOT_HELP', ('--help',): 'ROOT_HELP',\n  "
        "                ('solve','-h'): 'SOLVE_HELP', ('solve','--help'):"
        " 'SOLVE_HELP',\n                  ('verify','-h'): 'VERIFY_HELP', "
        "('verify','--help'): 'VERIFY_HELP'}\n    if tokens in help_forms:\n"
        "        return help_forms[tokens], None, ()\n    bad = ('usage', N"
        "one, ())\n    if not tokens or any(not x or '\\0' in x for x in tok"
        "ens):\n        return bad\n    if tokens[0] not in ('solve','verify"
        "'):\n        return bad\n    selection = None\n    operands = []\n   "
        ' ended = False\n    it = iter(tokens[1:])\n    for token in it:\n   '
        "     if not ended and token == '--':\n            ended = True\n   "
        "     elif not ended and token.startswith('-') and token != '-':\n "
        "           if tokens[0] != 'solve' or token != '--solver' or sele"
        'ction is not None:\n                return bad\n            selecti'
        "on = next(it, None)\n            if selection not in ('Standard','"
        "Accelerated'):\n                return bad\n        else:\n         "
        "   operands.append(token)\n    if tokens[0] == 'verify':\n        r"
        "eturn ('verify', None, tuple(operands)) if len(operands)==2 and o"
        "perands.count('-')<=1 else bad\n    return ('solve', selection or "
        "'Accelerated', tuple(operands)) if len(operands)==1 else bad\n"
    ),
}


_REFERENCE_HASHES = {
    'independent_wire': '95c1031fc387b765569fc381062384b8919a79f12128883becfc11ad7236bff6',
    'fixture_support': '1e5ef183cf99b7af88852027a8435cbd06c4db37e99fcc21a73edbc51edbc142',
    'fixture_mutations': '100b6c804e90835d73f36181ddd6255d5fc59537e1e324e0393fcea9a05ca3cd',
    'unit18_support': 'c546885198b658a589f0b949e3e35b33cb98ac59472a0d093503d715292a096a',
    'unit19_support': 'c405087222179627a885d50318680f9a9fa4f98a594d7227152bb45578f053fa',
}


_TABLE_PINS = (('U19_TEXT', 5, '5bb9c4a75c909327366a6c36a40723d5ebe58ae5e4fdcba3cad3724440dda8d5'),
 ('U19_ARGV', 98, '906f64979173ad552421e87dd3650e1899d19531482c174af5ade27c4a198a2d'),
 ('U19_PYTHON_CALL', 16, '031790291e747a76ed0503fcfa133ebcbb8b2cb39778cbbefcad9ba1ea39e560'),
 ('U19_INSTANCE_SYNTAX',
  52,
  '21a0ab5ea1e33475510dc8cd49a0ff796d122c78ead96cb4999b884f20720137'),
 ('U19_SOLVE_RESULT_SEAMS',
  22,
  'df4d5d2f793fa95759f3034584440573c97b834d9a9aa4390d7b373bdec34eaf'),
 ('U19_STREAMS', 10, 'a778a8aa42fae468b77643a0d3cf09d84e173cfc5f5caf0b13b9092e0a9072c0'),
 ('U19_PROMISE_FAULTS',
  40,
  '25addd3715fca597b4398118a7480ae43d6f5a97265578ab92732ae1a67565c3'),
 ('U19_EXCEPTIONS', 81, 'a62378a4f928d7195915435f550468736de62d98fd6f3dc09d3a912776a746ea'),
 ('U19_WRITE_PLANS', 21, '33e7adaecc789f0a2d7f3b4bc8025d81f6bd8bb4dfe23f5a6f2f9113e67af99b'),
 ('U19_PROCESS', 7, 'e91332762eecbcafc4f5b6b065105f6f0a5253c79afbb919c86d79786a22ea72'),
 ('U19_FAULTS', 30, '8d0c94d975b1cdddcc7f563168be31fa5c80f0c28607b4aea13192339bbe1171'),
 ('U19_PREFIXES', 2, 'ad677f717a1e30d07a7c95f1a5d6999ac3cf5bafd89591ca6519911a5c170493'),
 ('U19_INHERITANCE', 10, '7722d6e889f48f4ba65da6e6a7b42399fb6c6239ab4dc26106e677a43d6ab69a'),
 ('U19_COVERAGE', 18, '3671733916568330304d465ddd2b7fe346de3da24304569ed94b35dcd44ab34a'))


_PREFIX_PINS = ((3212040, '04ef6a4b38463aecb0d86731d1873aadb4acb8bc8a8593e0ea82b4325e56e7ac'),
 (3312641, '05255f65148c007278a38df664df5e6ff02db868d63fdafe7d9a016861952840'),
 (3392373, '523e3025e53fc1676ccd60a8e3e1f1955a8ace545ec34fea0cf4fa5d59dd056b'))


_CLOSED_PATHS = ('.gitignore',
 'CITATION.cff',
 'GOVERNING_SHA256SUMS.txt',
 'README.md',
 'docs/CONFORMANCE.md',
 'docs/CONTRACT.md',
 'docs/DESIGN.md',
 'docs/ORACLE_CATALOG.md',
 'docs/SPEC_LOCK.md',
 'docs/TEST_PLAN.md',
 'exactfrac/__init__.py',
 'exactfrac/_telemetry.py',
 'exactfrac/branch.py',
 'exactfrac/certificate.py',
 'exactfrac/families.py',
 'exactfrac/flow.py',
 'exactfrac/instance.py',
 'exactfrac/oracle.py',
 'exactfrac/parity_cut.py',
 'exactfrac/rational.py',
 'exactfrac/shore.py',
 'exactfrac/sign_routing.py',
 'exactfrac/solve.py',
 'exactfrac/telemetry.py',
 'exactfrac/witness.py',
 'exactfrac_verify/__init__.py',
 'exactfrac_verify/brute.py',
 'exactfrac_verify/check.py',
 'instances/MANIFEST',
 'pyproject.toml',
 'tests/_telemetry_source_audit.py',
 'tests/fixtures/unit16_legacy_sources.json',
 'tests/test_branch.py',
 'tests/test_branch_accelerated.py',
 'tests/test_certificate.py',
 'tests/test_families.py',
 'tests/test_flow.py',
 'tests/test_instance.py',
 'tests/test_oracle.py',
 'tests/test_parity_cut.py',
 'tests/test_rational.py',
 'tests/test_shore.py',
 'tests/test_sign_routing.py',
 'tests/test_solve.py',
 'tests/test_telemetry.py',
 'tests/test_verify_brute.py',
 'tests/test_verify_check.py',
 'tests/test_witness.py')


_FROZEN_SOURCE_HASHES = {
    '.gitignore': '5e8a2bb82c22d2c30a6d918e1f90e0b5d54112621aa45180d8ab2ff2b96f9ed9',
    'CITATION.cff': '8892be71dfb141b10be30b6d0683bfcff9167ac9dff7a8b0d99ea1b47f2fdbae',
    'GOVERNING_SHA256SUMS.txt': 'acc833e15e249d01fb8996507c80f9185c4cd49e5ff341960973fe051e4f46dd',
    'README.md': '05ff99bd562eaed86fe55e7eb2902255dacb4bddcbcb14943b21e2be7b51c09f',
    'exactfrac/__init__.py': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    'exactfrac/_telemetry.py': '3be3cae6757db921aacdde7fbae2cb59cfa1b91b73bd9c16c0695a1f620b9cac',
    'exactfrac/branch.py': '584d2f262c94e227f3832563aeceff600c95c6943b0401bd8ef64e3c2a5ef057',
    'exactfrac/certificate.py': 'cffab68bf6c9c6c6ef1d4f9cc177b9718298bf12ec5cc16b4ed3353728b318a4',
    'exactfrac/families.py': '92830c7cac7a6f39df5f16f316295352dee9e65bc31fe1220a85305cacd9872b',
    'exactfrac/flow.py': 'ee318ccbdfc59cadccd055dd1b57e016a1288387afb124792b52ce39c2b76fcc',
    'exactfrac/instance.py': '32695ee226d3636451d2964ee99bca0ed4cd9cc4a71542ffd435504a3918558e',
    'exactfrac/oracle.py': 'fa8885689608cc216e131cdc63573f698f628b1a9e313bde521e1f3feff88913',
    'exactfrac/parity_cut.py': 'f0cb4bbb38f80f05459c89662d3ee7fc3e09b63e1ca985ea37ccbfc9e0f85ec1',
    'exactfrac/rational.py': '933a1b79187bd8c93dddb8a93e9e92708775d980d2161f971a597a5f61a27a4b',
    'exactfrac/shore.py': '323fa6f5074a83dcedd16acadf8bc99905396298c7609cacab871f4dccab0415',
    'exactfrac/sign_routing.py': 'e0bd497b5034cee544332901d937f1973a6f37fbffb281337e4b091dabdb2beb',
    'exactfrac/solve.py': '46773d6f2247025220712e967315a33ff36bea60328bcc2b9b149d824f4d6e51',
    'exactfrac/telemetry.py': 'aadcbcd00fae3eba9e61a8433b90dae47ab0e67e91fa911cf57d909cef249bd3',
    'exactfrac/witness.py': '1225387644890efe4d70e9ede64d07b612b599f70c73b7de5378781fd17ceb6a',
    'exactfrac_verify/__init__.py': (
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    ),
    'exactfrac_verify/brute.py': 'b31e53a8b16a37ef8827141a78169ffe9b0a84762843a3ad45c89d9344f98bf6',
    'exactfrac_verify/check.py': '5beb9850bf7aeb311178a5f35df1357d8d4a3e801fde5341e2108176bd01f1ad',
    'pyproject.toml': '89977766c002fd79f1c75de93621062b4e7a042debe95ab9d238987fc9469da6',
    'tests/_telemetry_source_audit.py': (
        '7d737818adfb193c8335a123b4fdc38735260dd0006c4a0cdb9b5def945e1d77'
    ),
    'tests/fixtures/unit16_legacy_sources.json': (
        'e81ba1aac48412d7b9e85bb493d1edef1f98e6788d3ef67070b4a9ae21993136'
    ),
    'tests/test_branch.py': '47194d5905033b83d38df5a63a5e30405be307d027705fd96d8dca3d8569311f',
    'tests/test_branch_accelerated.py': (
        'e3b77951232df3b7faa7dafa581f023d00da26274f6c53c3139b8f591ff92e64'
    ),
    'tests/test_certificate.py': 'c94179fdbd3cb106394fd4780f5580664f41068facd65dc15a4f91b5d945a996',
    'tests/test_families.py': '60bf0ba2131ee9091eec7375207d516147d433085efe49b80bdc04df62e33fe9',
    'tests/test_flow.py': '2b006c77df22e9008cc4a69aef934d3c7f283f2880e089244668849e96b724ef',
    'tests/test_instance.py': '71d4ac06a8a91fc4f25fc5aaf27a60cc2b9af3cc9349b7332efa2565140a7ea0',
    'tests/test_oracle.py': '6cd667f7c3df33cff0265e72af730afa08275c29f732bfb64e8379650c43fd0c',
    'tests/test_parity_cut.py': '20c5b9bc371a2dfc18830b5266c0b429db71b38040ae47d3b142c0e5c070060a',
    'tests/test_rational.py': 'a30ca8fc17d967460e81499035ff4c74c654312517ebdc592e1211cf2f7fd6db',
    'tests/test_shore.py': 'c366e94e522a81f6f3b1b521a6c8c910c75898de30838a38511e540fa146ff40',
    'tests/test_sign_routing.py': (
        '740604855c8fb92b42d41e6eb6d530c445d0763f05dd0c201b218f520f743799'
    ),
    'tests/test_solve.py': '7cc5d67408a6779f738a0bb79d0f961919028bb77dce33e53b2a3f32832fa0b1',
    'tests/test_telemetry.py': 'a009f6e6052bf386793791a67a7973581c466968465d0d562eb5d4811096f94b',
    'tests/test_verify_brute.py': (
        '9d5f7e4bac733bc3c41cc6243fcb2fe36c228bab8c57a7de985cf7cac6d3e719'
    ),
    'tests/test_verify_check.py': (
        '99a66cef83df1c8c5191349e33966230ac21b8fc73e1e071f2f26bde74796dd3'
    ),
    'tests/test_witness.py': 'b3c9b1344afd0077822c6e460746fc55223919afd51ea65f4364e2e0a86d02c2',
}


_CLI_WORKER = (
    '"""Private execution harness; all commands call the actual candid'
    'ate CLI."""\nimport builtins\nimport hashlib\nimport importlib.abc\ni'
    'mport io\nimport json\nimport os\nfrom pathlib import Path\nimport sy'
    's\n\npayload = json.loads(sys.stdin.buffer.read())\nroot = Path(payl'
    "oad['root']).resolve()\nmode = payload['mode']\nlimit = sys.get_int"
    '_max_str_digits()\nrecursion = sys.getrecursionlimit()\nassert limi'
    "t == payload['limit']\nassert os.environ['PYTHONHASHSEED'] == payl"
    "oad['seed']\nassert not any(n.split('.')[0] in {'exactfrac', 'exac"
    "tfrac_verify', 'tests'} for n in sys.modules)\nsys.path.insert(0, "
    "str(root))\nallowed = {'exactfrac', 'exactfrac.cli'}\nif mode == 'v"
    "erify':\n    allowed |= {'exactfrac_verify', 'exactfrac_verify.che"
    "ck'}\nif mode == 'solve':\n    allowed |= {name for name in payload"
    "['project_names']}\nattempts = []\n\nclass Guard(importlib.abc.MetaP"
    'athFinder):\n    def find_spec(self, fullname, path=None, target=N'
    "one):\n        top = fullname.split('.')[0]\n        project = top "
    "in {'exactfrac', 'exactfrac_verify'}\n        private = top in {'t"
    "ests', 'fixture_support', 'fixture_mutations', 'independent_wire'"
    ",\n                          'unit18_support', 'unit19_support'}\n "
    '       if private or (project and fullname not in allowed):\n     '
    "       attempts.append(fullname)\n            raise ImportError('F"
    "orbidden CLI dependency: ' + fullname)\n        return None\n\nsys.m"
    'eta_path.insert(0, Guard())\nreal_open = builtins.open\nreal_stream'
    's = sys.stdin, sys.stdout, sys.stderr\n\nclass NoAccess:\n    @prope'
    "rty\n    def buffer(self):\n        raise AssertionError('Unexpecte"
    "d stream access')\n    def read(self, *args):\n        raise Assert"
    "ionError('Unexpected text read')\n    def write(self, *args):\n    "
    "    raise AssertionError('Unexpected text write')\n    def flush(s"
    "elf):\n        raise AssertionError('Unexpected text flush')\n    d"
    "ef close(self):\n        raise AssertionError('Caller-owned stream"
    " closed')\n\ndef forbidden_open(*args, **kwargs):\n    raise Asserti"
    "onError('Unexpected input access')\n\nbuiltins.open = forbidden_ope"
    'n\nsys.stdin = sys.stdout = sys.stderr = NoAccess()\ntry:\n    impor'
    't exactfrac.cli as cli\nfinally:\n    builtins.open = real_open\n   '
    ' sys.stdin, sys.stdout, sys.stderr = real_streams\nassert not atte'
    "mpts\nassert {n for n in sys.modules if n.split('.')[0] in {'exact"
    "frac', 'exactfrac_verify'}} <= {'exactfrac', 'exactfrac.cli'}\n\ncl"
    'ass Output:\n    def __init__(self):\n        self.data = bytearray'
    '()\n        self.flushes = 0\n    def write(self, raw):\n        sel'
    'f.data.extend(raw)\n        return len(raw)\n    def flush(self):\n '
    '       self.flushes += 1\n        return None\n    def close(self):'
    "\n        raise AssertionError('Output closed')\n\nclass Envelope(No"
    'Access):\n    def __init__(self, binary):\n        self.binary = bi'
    'nary\n    @property\n    def buffer(self):\n        return self.bina'
    'ry\n\nclass Input(io.BytesIO):\n    pass\n\ncalls = 0\nsolver_calls = 0'
    "\nlast_pair = None\nif mode == 'solve':\n    import exactfrac.solve "
    'as solver\n    original_solve = solver.solve\n    def observe_solve'
    '(instance, selection):\n        global solver_calls, last_pair\n   '
    '     solver_calls += 1\n        answer = original_solve(instance, '
    "selection)\n        last_pair = (format(answer[0].value.N, 'x'), f"
    "ormat(answer[0].value.D, 'x'))\n        return answer\n    solver.s"
    'olve = observe_solve\n\ndef run(argv, inputs, route):\n    global ca'
    'lls\n    queue = list(inputs)\n    readers = []\n    out, err = Outp'
    "ut(), Output()\n    def acquire(path, mode='r', *args, **kwargs):\n"
    "        assert mode == 'rb' and not args and not kwargs\n        e"
    'xpected_path, raw = queue.pop(0)\n        assert path == expected_'
    'path\n        reader = Input(raw)\n        readers.append(reader)\n '
    '       return reader\n    selected_out = Envelope(out) if route in'
    " {'solve', 'help'} else NoAccess()\n    selected_err = Envelope(er"
    "r) if route == 'usage' else NoAccess()\n    before = list(argv)\n  "
    '  builtins.open = acquire\n    sys.stdin, sys.stdout, sys.stderr ='
    ' NoAccess(), selected_out, selected_err\n    try:\n        calls +='
    ' 1\n        result = cli.main(argv)\n    finally:\n        builtins.'
    'open = real_open\n        sys.stdin, sys.stdout, sys.stderr = real'
    '_streams\n        assert argv == before and all(r.closed for r in '
    'readers)\n    assert not queue\n    assert type(result) is int\n    '
    'return result, bytes(out.data), bytes(err.data), out.flushes, err'
    ".flushes\n\naccepted = rejected = 0\noutputs = []\nif mode == 'help-u"
    "sage':\n    for key, argv, route, expected_out, expected_err, expe"
    "cted_code in payload['cases']:\n        result, out, err, of, ef ="
    ' run(argv, [], route)\n        assert (result, out.hex(), err.hex('
    ')) == (expected_code, expected_out, expected_err), key\n        as'
    "sert (of, ef) == ((0, 1) if route == 'usage' else (1, 0)), key\nel"
    "if mode == 'verify':\n    for key, ih, ch, good in payload['pairs'"
    "]:\n        inputs = [('i', bytes.fromhex(ih)), ('c', bytes.fromhe"
    "x(ch))]\n        try:\n            answer = run(['verify', 'i', 'c'"
    "], inputs, 'verify')\n        except ValueError:\n            asser"
    't good is False, key\n            rejected += 1\n        else:\n    '
    "        assert good is True and answer == (0, b'', b'', 0, 0), ke"
    "y\n            accepted += 1\nelif mode == 'solve':\n    for key, ih"
    " in payload['instances']:\n        raw = bytes.fromhex(ih)\n       "
    " for selection in ('Standard', 'Accelerated'):\n            observ"
    'ed = []\n            for repeat in (0, 1):\n                before '
    '= solver_calls\n                status, out, err, of, ef = run(\n  '
    "                  ['solve', '--solver', selection, 'i'], [('i', r"
    "aw)], 'solve')\n                assert solver_calls == before + 1\n"
    "                assert (status, err, of, ef) == (0, b'', 1, 0)\n  "
    '              observed.append(out)\n                if repeat == 0'
    ':\n                    outputs.append((key, selection, out.hex(), '
    'last_pair))\n            assert observed[0] == observed[1]\nassert '
    'not attempts\nassert sys.get_int_max_str_digits() == limit and sys'
    '.getrecursionlimit() == recursion\norigins = {}\nfor name, module i'
    "n sorted(sys.modules.items()):\n    if name.split('.')[0] in {'exa"
    "ctfrac', 'exactfrac_verify'}:\n        assert name in allowed\n    "
    '    path = Path(module.__file__).resolve()\n        relative = str'
    '(path.relative_to(root))\n        digest = hashlib.sha256(path.rea'
    "d_bytes()).hexdigest()\n        assert digest == payload['files']["
    "relative]\n        origins[name] = relative\nprint(json.dumps({'mod"
    "e': mode, 'calls': calls, 'solver_calls': solver_calls,\n         "
    "         'accepted': accepted, 'rejected': rejected, 'outputs': o"
    "utputs,\n                  'limit': limit, 'seed': payload['seed']"
    ", 'settings_unchanged': True,\n                  'forbidden_import"
    "_attempts': attempts, 'project_imports': origins}, sort_keys=True"
    '))\n'
)


_REFERENCE_WORKER = (
    'import builtins\nimport hashlib\nimport importlib.abc\nimport json\ni'
    'mport os\nimport sys\nimport types\n\npayload = json.loads(sys.stdin.'
    'buffer.read())\nlimit, recursion = sys.get_int_max_str_digits(), s'
    "ys.getrecursionlimit()\nassert limit == payload['limit'] and os.en"
    "viron['PYTHONHASHSEED'] == payload['seed']\nattempts = []\nclass Gu"
    'ard(importlib.abc.MetaPathFinder):\n    def find_spec(self, fullna'
    "me, path=None, target=None):\n        if fullname.split('.')[0] in"
    " {'exactfrac', 'exactfrac_verify', 'tests'}:\n            attempts"
    ".append(fullname)\n            raise ImportError('Reference proces"
    "s forbids project dependencies')\n        return None\nsys.meta_pat"
    "h.insert(0, Guard())\nsource = payload['source']\nassert hashlib.sh"
    "a256(source.encode()).hexdigest() == payload['source_sha256']\nmod"
    "ule = types.ModuleType('unit19_independent_wire_reference')\nexec("
    "compile(source, '<independent-wire>', 'exec'), module.__dict__)\na"
    "ccepted = rejected = 0\nfor key, ih, ch, good in payload['pairs']:"
    '\n    try:\n        module.verify(bytes.fromhex(ih), bytes.fromhex('
    'ch))\n    except ValueError:\n        assert not good, key\n        '
    'rejected += 1\n    else:\n        assert good, key\n        accepted'
    " += 1\nassert not attempts\nassert not any(n.split('.')[0] in {'exa"
    "ctfrac', 'exactfrac_verify', 'tests'} for n in sys.modules)\nasser"
    't sys.get_int_max_str_digits() == limit and sys.getrecursionlimit'
    "() == recursion\nprint(json.dumps({'accepted': accepted, 'rejected"
    "': rejected, 'limit': limit,\n                  'seed': payload['s"
    "eed'], 'project_imports': [],\n                  'forbidden_import"
    "_attempts': [], 'settings_unchanged': True}, sort_keys=True))\n"
)



def _load_references():
    modules = {}
    original_import = builtins.__import__

    def reference_import(name, globals=None, locals=None, fromlist=(), level=0):
        if level == 0 and name in modules:
            return modules[name]
        assert name.split(".")[0] not in {"exactfrac", "exactfrac_verify", "tests"}
        return original_import(name, globals, locals, fromlist, level)

    for name, source in _REFERENCE_SOURCES.items():
        assert _sha(source.encode("utf-8")) == _REFERENCE_HASHES[name]
        module = types.ModuleType(name)
        module.__dict__["__builtins__"] = dict(vars(builtins), __import__=reference_import)
        exec(compile(source, "<unit19-independent-" + name + ">", "exec"), module.__dict__)
        modules[name] = module
    return modules


_REFS = _load_references()
_F = _REFS["fixture_support"]
_U18 = _REFS["unit18_support"]
_U19 = _REFS["unit19_support"]
_W = _REFS["independent_wire"]
_TABLES = _U19.tables_at(_CATALOGUE)
_GRAPHS = _U18.all_graphs(_TABLES)
_GRAPH_BY_ID = dict(_GRAPHS)
_LITERALS = _U18.literals(_TABLES)
_WIRE = _U18.wire_cases(_TABLES)
_TEXT = {key: _U19.bytes_recipe(parts) for key, parts, _, _ in _TABLES["U19_TEXT"]}
_ORIGINAL_FROM_DICT = _instance.Instance.from_dict
_ORIGINAL_SOLVE = _solver.solve
_ORIGINAL_BUILD = _certificate.build_certificate
_ORIGINAL_SERIALIZE = _certificate.serialize_certificate
_ORIGINAL_VERIFY = _checker.verify_certificate
_DEFAULT_LITERAL = "U18/PAIR-FULL"
_DEFAULT_INPUT, _DEFAULT_CERT, _ = _LITERALS[_DEFAULT_LITERAL]
_DEFAULT_GRAPH = _W.parse_instance(_DEFAULT_INPUT)
_MISSING = object()


def _literal_result(key):
    instance_bytes, certificate_bytes, _ = _LITERALS[key]
    graph = _W.parse_instance(instance_bytes)
    obj = _W.verify(instance_bytes, certificate_bytes)
    witness = None
    if not obj["empty"]:
        dense = [0] * len(graph["edges"])
        for ref, count in obj["y"]:
            dense[ref] = count
        witness = Witness(sum(1 << vertex for vertex in obj["U"]), tuple(dense))
    result = _solver.SolveResult(ExactValue(obj["N"], obj["D"]), witness)
    return result


class _BytesSubclass(bytes):
    pass


class _StringSubclass(str):
    pass


class _ListSubclass(list):
    pass


class _TupleSubclass(tuple):
    pass


class _DictSubclass(dict):
    pass


class _IntSubclass(int):
    pass


class _InstanceSubclass(_instance.Instance):
    pass


class _ResultSubclass(_solver.SolveResult):
    pass


class _StatsSubclass(_solver.SolveStats):
    pass


class _Reader:
    def __init__(self, harness, label, raw, owned):
        self.harness = harness
        self.label = label
        self.raw = raw
        self.owned = owned
        self.reads = 0
        self.position = 0
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.close()
        return False

    def read(self, size=-1):
        assert type(size) is int and size >= -1
        assert not self.closed
        self.reads += 1
        assert self.reads <= len(self.raw) + 2, "Input reads made no progress"
        h = self.harness
        if self.reads == 1:
            h.events.append(("read", self.label))
        end = len(self.raw) if size == -1 else min(len(self.raw), self.position + size)
        part = self.raw[self.position:end]
        self.position = end
        site = "stdin read" if self.label == "stdin" else "file read"
        return h.at(site, lambda: h.at("reader", lambda: part))

    def close(self):
        assert self.owned, "Process stdin was closed"
        assert not self.closed, "Owned input closed more than once"
        self.closed = True
        self.harness.events.append(("close", self.label))
        return self.harness.at("file close", lambda: None)


class _Writer:
    def __init__(self, harness, label):
        self.harness = harness
        self.label = label
        self.output = bytearray()
        self.writes = []
        self.flushes = 0
        self.plan = []
        self.unit_writes = False
        self.fault_count = _MISSING
        self.fault_flush = _MISSING

    def write(self, data):
        raw = memoryview(data).tobytes()
        assert raw, "An empty write has no progress to make"
        self.writes.append(raw)
        assert len(self.writes) < 100_000, "Writer failed to make bounded progress"
        h = self.harness
        h.events.append(("write", self.label))
        h.at(self.label + " write", lambda: None)
        if self.fault_count is not _MISSING:
            return self.fault_count(len(raw))
        token = self.plan.pop(0) if self.plan else ("one" if self.unit_writes else "remaining")
        if isinstance(token, BaseException):
            raise token
        count = {"one": 1, "two": 2, "remaining": len(raw)}[token]
        count = min(count, len(raw))
        self.output.extend(raw[:count])
        return count

    def flush(self):
        self.flushes += 1
        self.harness.events.append(("flush", self.label))
        self.harness.at(self.label + " flush", lambda: None)
        return None if self.fault_flush is _MISSING else self.fault_flush

    def close(self):
        raise AssertionError("Caller-owned output was closed")


class _Envelope:
    def __init__(self, harness, label, binary, allowed):
        self.harness = harness
        self.label = label
        self.binary = binary
        self.allowed = allowed
        self.accesses = 0

    @property
    def buffer(self):
        h = self.harness
        self.accesses += 1
        h.events.append(("buffer", self.label))
        h.at("sys." + self.label + ".buffer", lambda: None)
        assert self.allowed, "Forbidden process-stream access: " + self.label
        if self.label == "stdout" and h.command == "solve":
            assert h.verified, "stdout accessed before successful self-check"
        return self.binary

    def write(self, _data):
        raise AssertionError("Text output fallback")

    def read(self, *_args):
        raise AssertionError("Text input fallback")

    def flush(self):
        raise AssertionError("Text stream flush instead of binary stream")

    def close(self):
        raise AssertionError("Process stream envelope was closed")


class _Harness:
    """Instrument only named dependencies and host streams, never the CLI itself."""

    def __init__(self, command="solve", selection="Accelerated", literal=_DEFAULT_LITERAL):
        self.command = command
        self.selection = selection
        self.input_bytes, self.certificate_bytes, _ = _LITERALS[literal]
        self.literal = literal
        self.expected_graph = _W.parse_instance(self.input_bytes)
        self.result = _literal_result(literal)
        self.stats = _solver.SolveStats(
            selection, (), "Empty" if self.result.witness is None else "Baseline"
        )
        self.events = []
        self.calls = Counter()
        self.import_attempts = []
        self.faults = {}
        self.file_inputs = []
        self.readers = []
        self.instance = None
        self.returned_result = None
        self.object = None
        self.emitted = None
        self.verified = False
        self.real_solve = False
        self.stdout = _Writer(self, "stdout")
        self.stderr = _Writer(self, "stderr")
        self.streams = None

    def at(self, site, normal):
        self.calls[site] += 1
        override = self.faults.get(site, _MISSING)
        if isinstance(override, BaseException):
            raise override
        return normal() if override is _MISSING else override

    def open(self, file, mode="r", *args, **kwargs):
        path = file
        assert type(path) is str, "Do not normalize or coerce the supplied operand"
        assert mode == "rb", "Inputs require read-only binary mode"
        assert not any(kwargs.get(k) for k in ("encoding", "errors", "newline"))
        self.events.append(("open", path))
        self.at("file open", lambda: None)
        assert self.file_inputs, "Unexpected named input access: " + path
        expected_path, raw = self.file_inputs.pop(0)
        assert path == expected_path
        if isinstance(raw, BaseException):
            raise raw
        reader = _Reader(self, path, raw, True)
        self.readers.append(reader)
        return reader

    def install_io(self, patch, operands=()):
        for index, operand in enumerate(operands):
            raw = self.input_bytes if index == 0 else self.certificate_bytes
            if operand != "-":
                self.file_inputs.append((operand, raw))
        stdin_bytes = self.input_bytes
        if self.command == "verify" and len(operands) == 2 and operands[1] == "-":
            stdin_bytes = self.certificate_bytes
        stdin = _Reader(self, "stdin", stdin_bytes, False)
        self.stdin = stdin
        self.streams = (
            _Envelope(self, "stdin", stdin, "-" in operands),
            _Envelope(self, "stdout", self.stdout, self.command in {"solve", "help"}),
            _Envelope(self, "stderr", self.stderr, self.command == "usage"),
        )
        patch.setattr(builtins, "open", self.open)
        patch.setattr(io, "open", self.open)
        for name, stream in zip(("stdin", "stdout", "stderr"), self.streams, strict=True):
            patch.setattr(sys, name, stream)

    def install_dependencies(self, patch):
        h = self

        def from_dict(cls, obj):
            assert h.command == "solve"
            h.events.append(("from_dict",))
            assert type(obj) is dict and obj == h.expected_graph
            result = h.at("from_dict", lambda: _ORIGINAL_FROM_DICT(obj))
            h.instance = result
            return result

        def solve(instance, branch_solver):
            assert h.command == "solve" and instance is h.instance
            assert branch_solver == h.selection and type(branch_solver) is str
            h.events.append(("solve", branch_solver))
            normal = (
                (lambda: _ORIGINAL_SOLVE(instance, branch_solver))
                if h.real_solve else (lambda: (h.result, h.stats))
            )
            pair = h.at("solve", normal)
            if type(pair) is tuple and len(pair) == 2:
                h.returned_result = pair[0]
            return pair

        def build(instance, result):
            assert h.command == "solve" and instance is h.instance
            assert result is h.returned_result
            h.events.append(("build",))
            obj = h.at("build", lambda: _ORIGINAL_BUILD(instance, result))
            h.object = obj
            return obj

        def serialize(instance, obj):
            assert h.command == "solve" and instance is h.instance and obj is h.object
            h.events.append(("serialize",))
            raw = h.at("serialize", lambda: _ORIGINAL_SERIALIZE(instance, obj))
            h.emitted = raw
            return raw

        def verify(ib, cb):
            assert h.command in {"solve", "verify"}
            assert type(ib) is bytes and ib == h.input_bytes
            expected = h.emitted if h.command == "solve" else h.certificate_bytes
            assert type(cb) is bytes and cb == expected
            h.events.append(("verify",))
            answer = h.at("verify", lambda: _ORIGINAL_VERIFY(ib, cb))
            h.verified = answer is None
            return answer

        def forbidden(*_args, **_kwargs):
            raise AssertionError("Forbidden normalization/telemetry dependency")

        patch.setattr(_instance.Instance, "from_dict", classmethod(from_dict))
        patch.setattr(_instance.Instance, "from_records", forbidden)
        patch.setattr(_solver, "solve", solve)
        patch.setattr(_certificate, "build_certificate", build)
        patch.setattr(_certificate, "serialize_certificate", serialize)
        patch.setattr(_checker, "verify_certificate", verify)
        if h.command != "solve":
            original_import = builtins.__import__
            allowed = {"exactfrac", "exactfrac.cli"}
            if h.command == "verify":
                allowed.update({"exactfrac_verify", "exactfrac_verify.check"})

            def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
                resolved = name
                if level:
                    package = (globals or {}).get("__package__", "").split(".")
                    base = ".".join(package[:len(package) - level + 1])
                    resolved = base + ("." + name if name else "")
                requested = [resolved]
                if resolved in {"exactfrac", "exactfrac_verify"}:
                    requested.extend(resolved + "." + item for item in (fromlist or ()))
                for module in requested:
                    if (
                        module.split(".")[0] in {"exactfrac", "exactfrac_verify"}
                        and module not in allowed
                    ):
                        h.import_attempts.append(module)
                        raise AssertionError("Premature or forbidden command import: " + module)
                return original_import(name, globals, locals, fromlist, level)

            patch.setattr(builtins, "__import__", guarded_import)

    def conserved(self):
        assert self.streams is not None
        assert not self.import_attempts
        assert (sys.stdin, sys.stdout, sys.stderr) == self.streams
        assert not self.stdin.closed
        assert all(reader.closed for reader in self.readers)


def _call(harness, argv, monkeypatch):
    before = copy.deepcopy(argv)
    with monkeypatch.context() as patch:
        harness.install_io(patch, tuple(_operands_for_harness(harness, argv)))
        harness.install_dependencies(patch)
        answer = _cli.main(argv)
        harness.conserved()
    assert argv == before
    return answer


def _operands_for_harness(harness, argv):
    # Only harness callers use this explicit attachment, never parse argv here.
    del argv
    return getattr(harness, "operands", ())


def _assert_success(harness, answer, expected):
    assert type(answer) is int and answer == (2 if harness.command == "usage" else 0)
    writer = harness.stderr if harness.command == "usage" else harness.stdout
    assert bytes(writer.output) == expected
    if harness.command == "verify":
        assert harness.streams[1].accesses == harness.streams[2].accesses == 0
    else:
        assert writer.flushes == 1
    other = harness.stdout if harness.command == "usage" else harness.stderr
    assert not other.writes and not other.flushes
    assert not harness.file_inputs


def test_exact_public_surface_and_invocation_contract():
    assert _cli.__all__ == ("main",)
    assert {name for name, value in vars(_cli).items()
            if not name.startswith("_") and callable(value)
            and getattr(value, "__module__", None) == _cli.__name__} == {"main"}
    parameters = inspect.signature(_cli.main).parameters
    assert list(parameters) == ["argv"]
    assert parameters["argv"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert parameters["argv"].default is None
    assert get_type_hints(_cli.main) == {"argv": list[str] | None, "return": int}


@pytest.mark.parametrize("row", _TABLES["U19_ARGV"], ids=[r[0] for r in _TABLES["U19_ARGV"]])
def test_registered_argv_grammar_and_literal_paths(row, monkeypatch):
    _, tokens, kind, route, operands, stdout, stderr, status, _ = row
    command = "help" if kind.endswith("_HELP") else kind
    h = _Harness(command, route or "Accelerated")
    h.operands = operands
    answer = _call(h, list(tokens), monkeypatch)
    expected = h.certificate_bytes if stdout == "EMITTED_CERTIFICATE" else _TEXT[stdout]
    if command == "usage":
        expected = _TEXT[stderr]
    _assert_success(h, answer, expected)
    assert answer == status
    if command == "solve":
        assert [e[0] for e in h.events if e[0] in {
            "from_dict", "solve", "build", "serialize", "verify"
        }] == ["from_dict", "solve", "build", "serialize", "verify"]
        assert all(h.calls[s] == 1 for s in ("from_dict", "solve", "build", "serialize", "verify"))
    elif command == "verify":
        assert h.calls["verify"] == 1
        assert not any(h.calls[s] for s in ("from_dict", "solve", "build", "serialize"))
    else:
        assert not any(e[0] in {"open", "read", "from_dict", "solve", "verify"} for e in h.events)


def _python_argument(description):
    tag, *rest = description
    if tag == "tuple":
        return tuple(rest[0])
    if tag in {"bytes", "str", "bool", "int"}:
        return {"bytes": lambda: rest[0].encode(), "str": lambda: rest[0],
                "bool": lambda: rest[0], "int": lambda: rest[0]}[tag]()
    if tag == "dict":
        return {}
    if tag == "list-subclass":
        return _ListSubclass(rest[0])
    if tag == "iterator":
        return iter(rest[0])
    if tag == "list":
        value = rest[0]
        if value is None:
            return [None]
        kind, item = value
        return [{"str-subclass": lambda: _StringSubclass(item),
                 "bytes": lambda: item.encode(), "bool": lambda: item}[kind]()]
    raise AssertionError("Unhandled registered Python argument")


@pytest.mark.parametrize(
    "row", _TABLES["U19_PYTHON_CALL"], ids=[r[0] for r in _TABLES["U19_PYTHON_CALL"]]
)
def test_python_call_exact_types_and_native_arity(row, monkeypatch):
    key, description, *_ = row
    h = _Harness("help" if key in {"NONE-SNAPSHOT", "KEYWORD"} else "invalid-python")
    with monkeypatch.context() as patch:
        h.install_io(patch)
        h.install_dependencies(patch)
        if key == "NONE-SNAPSHOT":
            process_argv = ["irrelevant-program-name", "--help"]
            patch.setattr(sys, "argv", process_argv)
            answer = _cli.main(None)
            assert process_argv == ["irrelevant-program-name", "--help"]
            _assert_success(h, answer, _TEXT["ROOT_HELP"])
        elif key == "KEYWORD":
            answer = _cli.main(argv=["--help"])
            _assert_success(h, answer, _TEXT["ROOT_HELP"])
        else:
            expected = TypeError if key in {"ARITY", "UNKNOWN-KW"} else ValueError
            with pytest.raises(expected) as caught:
                if key == "ARITY":
                    _cli.main([], [])
                elif key == "UNKNOWN-KW":
                    _cli.main(unknown=[])
                else:
                    _cli.main(_python_argument(description))
            assert type(caught.value) is expected
            assert not h.events
        h.conserved()


@pytest.mark.parametrize(
    "row", _TABLES["U19_INSTANCE_SYNTAX"], ids=[r[0] for r in _TABLES["U19_INSTANCE_SYNTAX"]]
)
def test_registered_instance_syntax_and_graph_boundary(row, monkeypatch):
    _, gid, parts, size, digest, category, _, decoded_fingerprint = row
    raw = _U19.bytes_recipe(parts)
    assert len(raw) == size and _sha(raw) == digest
    h = _Harness()
    h.input_bytes = raw
    h.operands = ("i",)
    if category == "valid":
        h.expected_graph = _W.parse_instance(raw)
        assert h.expected_graph == _GRAPH_BY_ID[gid]
        assert _sha(_F.encode(_GRAPH_BY_ID[gid])) == decoded_fingerprint
        h.real_solve = True
        answer = _call(h, ["solve", "i"], monkeypatch)
        assert type(answer) is int and answer == 0
        obj = _W.verify(raw, bytes(h.stdout.output))
        assert (obj["N"], obj["D"]) == (h.returned_result.value.N, h.returned_result.value.D)
        assert h.calls["from_dict"] == 1
    else:
        expected = (
            _instance.UnsupportedInstance
            if category == "unsupported" else _instance.InvalidInstance
        )
        seen = []
        h.faults["solve"] = AssertionError("Solver reached after rejected input")
        with monkeypatch.context() as patch:
            h.install_io(patch, ("i",))
            h.install_dependencies(patch)

            def observe(cls, obj):
                seen.append(copy.deepcopy(obj))
                return _ORIGINAL_FROM_DICT(obj)

            patch.setattr(_instance.Instance, "from_dict", classmethod(observe))
            with pytest.raises(expected) as caught:
                _cli.main(["solve", "i"])
            assert type(caught.value) is expected
            h.conserved()
        assert len(seen) == (0 if category == "syntax" else 1)
        assert h.streams[1].accesses == h.streams[2].accesses == 0
        assert not h.calls["solve"]


@pytest.mark.parametrize("route", _ROUTES)
@pytest.mark.parametrize(
    "row", _TABLES["U19_SOLVE_RESULT_SEAMS"], ids=[r[0] for r in _TABLES["U19_SOLVE_RESULT_SEAMS"]]
)
def test_fixed_literal_solve_result_seams_preserve_raw_identity(row, route, monkeypatch):
    key, _, numerator, denominator, *_ = row
    h = _Harness("solve", route, key)
    h.operands = ("i",)
    answer = _call(h, ["solve", "--solver", route, "i"], monkeypatch)
    _assert_success(h, answer, h.certificate_bytes)
    obj = _W.verify(h.input_bytes, bytes(h.stdout.output))
    assert (obj["N"], obj["D"]) == (_F.number(numerator), _F.number(denominator))
    assert h.returned_result is h.result


@pytest.mark.parametrize("row", _WIRE, ids=[r[0] for r in _WIRE])
def test_complete_fixed_wire_corpus_through_verify(row, monkeypatch):
    _, ib, cb, accepted, _ = row
    h = _Harness("verify")
    h.input_bytes, h.certificate_bytes = ib, cb
    with monkeypatch.context() as patch:
        h.install_io(patch, ("i", "c"))
        h.install_dependencies(patch)
        if accepted:
            result = _cli.main(["verify", "i", "c"])
            _assert_success(h, result, b"")
            _W.verify(ib, cb)
        else:
            with pytest.raises(ValueError):
                _W.verify(ib, cb)
            with pytest.raises(ValueError):
                _cli.main(["verify", "i", "c"])
        h.conserved()
        assert h.calls["verify"] == 1
        assert h.streams[1].accesses == h.streams[2].accesses == 0
        assert [e for e in h.events if e[0] in {"open", "read", "close", "verify"}] == [
            ("open", "i"), ("read", "i"), ("close", "i"),
            ("open", "c"), ("read", "c"), ("close", "c"), ("verify",),
        ]



def _bad_normal(h, site, descriptor):
    basic = {
        "None": None, "plain object": object(), "str": "not bytes", "bytearray": bytearray(b"x"),
        "bytes-subclass": _BytesSubclass(b"x"), "False": False, "True": True,
        "0": 0, "dict": {}, "list": [], "dict-subclass": _DictSubclass(),
    }
    if descriptor in basic:
        return basic[descriptor]
    if descriptor == "Instance-subclass":
        g = h.expected_graph
        return _InstanceSubclass(g["n"], tuple(tuple(e) for e in g["edges"]), tuple(g["f"]))
    if descriptor == "SolveResult-subclass":
        return _ResultSubclass(h.result.value, h.result.witness)
    if descriptor == "SolveStats-subclass":
        return _StatsSubclass(h.selection, (), "Baseline")
    if descriptor == "other legal selection":
        other = "Standard" if h.selection == "Accelerated" else "Accelerated"
        return _solver.SolveStats(other, (), "Baseline")
    if site == "solve outer":
        pair = (h.result, h.stats)
        return {
            "list pair": list(pair), "tuple subclass": _TupleSubclass(pair),
            "tuple length one": pair[:1], "tuple length three": (*pair, None),
        }[descriptor]
    raise AssertionError("Unmapped normal-return fixture: " + descriptor)


def _write_fault(descriptor):
    return {
        "None": lambda _size: None,
        "False": lambda _size: False,
        "True": lambda _size: True,
        "zero": lambda _size: 0,
        "negative": lambda _size: -1,
        "remaining plus one": lambda size: size + 1,
        "int-subclass": lambda size: _IntSubclass(size),
    }[descriptor]


@pytest.mark.parametrize(
    "row", _TABLES["U19_PROMISE_FAULTS"], ids=[r[0] for r in _TABLES["U19_PROMISE_FAULTS"]]
)
def test_closed_normal_return_promises_fail_before_downstream_work(row, monkeypatch):
    _, site, descriptor, _, _ = row
    h = _Harness()
    stages = ["reader", "from_dict", "solve", "build", "serialize", "verify"]
    if site == "write return":
        h.stdout.fault_count = _write_fault(descriptor)
    elif site == "flush return":
        h.stdout.fault_flush = _bad_normal(h, site, descriptor)
    else:
        value = _bad_normal(h, site, descriptor)
        name = site
        if site == "solve outer":
            name = "solve"
        elif site == "solve result":
            name, value = "solve", (value, h.stats)
        elif site in {"solve stats", "stats.branch_solver"}:
            name, value = "solve", (h.result, value)
        elif site == "verify normal return":
            name = "verify"
        h.faults[name] = value
    with monkeypatch.context() as patch:
        h.install_io(patch, ("i",))
        h.install_dependencies(patch)
        with pytest.raises(RuntimeError) as caught:
            _cli.main(["solve", "i"])
        assert type(caught.value) is RuntimeError
        h.conserved()
    if site not in {"write return", "flush return"}:
        boundary = stages.index(name)
        assert h.calls[name] == 1
        assert all(h.calls[later] == 0 for later in stages[boundary + 1:])
        assert h.streams[1].accesses == 0
    elif site == "write return":
        assert len(h.stdout.writes) == 1 and h.stdout.flushes == 0
    else:
        assert len(h.stdout.writes) == 1 and h.stdout.flushes == 1
    assert h.streams[2].accesses == 0


@pytest.mark.parametrize("value", [False, 0, {}, object()], ids=["false", "zero", "dict", "object"])
def test_verify_command_requires_exact_none_without_stream_access(value, monkeypatch):
    h = _Harness("verify")
    h.faults["verify"] = value
    with monkeypatch.context() as patch:
        h.install_io(patch, ("i", "c"))
        h.install_dependencies(patch)
        with pytest.raises(RuntimeError) as caught:
            _cli.main(["verify", "i", "c"])
        assert type(caught.value) is RuntimeError
        h.conserved()
    assert h.calls["verify"] == 1
    assert h.streams[1].accesses == h.streams[2].accesses == 0


def _injected_exception(name):
    classes = dict(vars(builtins), InvalidInstance=_instance.InvalidInstance,
                   UnsupportedInstance=_instance.UnsupportedInstance)
    return classes[name]("unit19 injected operational exception")


@pytest.mark.parametrize(
    "row", _TABLES["U19_EXCEPTIONS"], ids=[r[0] for r in _TABLES["U19_EXCEPTIONS"]]
)
def test_registered_operational_exceptions_preserve_identity(row, monkeypatch):
    _, site, exception_name, *_ = row
    command = "solve"
    argv, operands = ["solve", "i"], ("i",)
    mapped = site
    if site == "verify command":
        command, argv, operands, mapped = "verify", ["verify", "i", "c"], ("i", "c"), "verify"
    elif site == "self-check":
        mapped = "verify"
    elif site == "help write":
        command, argv, operands, mapped = "help", ["--help"], (), "stdout write"
    elif site in {"usage flush", "sys.stderr.buffer"}:
        command, argv, operands = "usage", [], ()
        mapped = "stderr flush" if site == "usage flush" else site
    elif site in {"stdin read", "sys.stdin.buffer"}:
        argv, operands = ["solve", "-"], ("-",)
    elif site == "read":
        mapped = "file read"
    h = _Harness(command)
    exc = _injected_exception(exception_name)
    h.faults[mapped] = exc
    with monkeypatch.context() as patch:
        h.install_io(patch, operands)
        h.install_dependencies(patch)
        if site == "JSON substrate":
            def broken_json(*_args, **_kwargs):
                h.calls["JSON substrate"] += 1
                raise exc

            patch.setattr(json, "loads", broken_json)
        with pytest.raises(type(exc)) as caught:
            _cli.main(argv)
        assert caught.value is exc
        h.conserved()
    assert h.calls[mapped] == 1
    if site not in {"stdout write", "stdout flush", "help write", "sys.stdout.buffer"}:
        assert h.streams[1].accesses == 0
    if command != "usage":
        assert h.streams[2].accesses == 0
    if site not in {"stdout flush", "usage flush"}:
        assert not h.stdout.flushes and not h.stderr.flushes


@pytest.mark.parametrize("site", ["file read", "solve", "build", "serialize", "verify"])
def test_syntax_exception_classes_are_not_translated_outside_decoders(site, monkeypatch):
    for exc in (
        UnicodeDecodeError("utf-8", b"\xff", 0, 1, "injected downstream"),
        json.JSONDecodeError("injected downstream", "", 0),
    ):
        h = _Harness()
        h.faults[site] = exc
        with monkeypatch.context() as patch:
            h.install_io(patch, ("i",))
            h.install_dependencies(patch)
            with pytest.raises(type(exc)) as caught:
                _cli.main(["solve", "i"])
            assert caught.value is exc
            h.conserved()
        assert h.streams[1].accesses == 0


def test_actual_json_substrate_decode_error_has_the_ruled_translation(monkeypatch):
    exc = json.JSONDecodeError("injected at the JSON operation", "", 0)
    h = _Harness()
    with monkeypatch.context() as patch:
        h.install_io(patch, ("i",))
        h.install_dependencies(patch)

        def decode_failure(*_args, **_kwargs):
            raise exc

        patch.setattr(json, "loads", decode_failure)
        with pytest.raises(_instance.InvalidInstance) as caught:
            _cli.main(["solve", "i"])
        assert type(caught.value) is _instance.InvalidInstance
        assert caught.value is not exc
        h.conserved()
    assert h.streams[1].accesses == 0


@pytest.mark.parametrize(
    "row", _TABLES["U19_WRITE_PLANS"], ids=[r[0] for r in _TABLES["U19_WRITE_PLANS"]]
)
def test_registered_short_write_progress_flush_and_partial_failure(row, monkeypatch):
    key, route, _, _, _ = row
    command = {"root-help": "help", "usage": "usage", "solve": "solve"}[route]
    h = _Harness(command)
    argv = {"help": ["--help"], "usage": [], "solve": ["solve", "i"]}[command]
    operands = ("i",) if command == "solve" else ()
    expected = h.certificate_bytes if command == "solve" else _TEXT[
        "ROOT_HELP" if command == "help" else "USAGE_ERROR"
    ]
    writer = h.stderr if command == "usage" else h.stdout
    exc = OSError("selected binary operation failed")
    suffix = key.removeprefix(route + "-")
    if suffix == "SHORT":
        writer.plan = ["one", "two", "remaining"]
    elif suffix == "UNIT":
        writer.unit_writes = True
    elif suffix == "FAIL-AFTER-PREFIX":
        writer.plan = ["two", exc]
    elif suffix == "FLUSH-FAIL":
        h.faults[writer.label + " flush"] = exc
    elif suffix == "BAD-COUNT":
        writer.fault_count = lambda _size: 0
    elif suffix == "BAD-FLUSH":
        writer.fault_flush = False
    with monkeypatch.context() as patch:
        h.install_io(patch, operands)
        h.install_dependencies(patch)
        if suffix in {"FAIL-AFTER-PREFIX", "FLUSH-FAIL"}:
            with pytest.raises(OSError) as caught:
                _cli.main(argv)
            assert caught.value is exc
        elif suffix in {"BAD-COUNT", "BAD-FLUSH"}:
            with pytest.raises(RuntimeError) as caught:
                _cli.main(argv)
            assert type(caught.value) is RuntimeError
        else:
            _assert_success(h, _cli.main(argv), expected)
        h.conserved()
    if suffix == "FAIL-AFTER-PREFIX":
        assert bytes(writer.output) == expected[:2]
        assert writer.writes == [expected, expected[2:]]
        assert writer.flushes == 0
    elif suffix == "BAD-COUNT":
        assert writer.writes == [expected] and writer.flushes == 0
    else:
        assert bytes(writer.output) == expected and writer.flushes == 1
        if suffix == "SHORT":
            assert writer.writes == [expected, expected[1:], expected[3:]]
        elif suffix == "UNIT":
            assert writer.writes == [expected[i:] for i in range(len(expected))]
        else:
            assert writer.writes == [expected]


@pytest.mark.parametrize("which", ["instance", "certificate"])
def test_verify_operand_acquisition_precedes_checker_validation(which, monkeypatch):
    h = _Harness("verify")
    h.input_bytes = b"this is not JSON\n"
    exc = OSError("unreadable operand")
    with monkeypatch.context() as patch:
        h.install_io(patch, ("bad-i", "bad-c"))
        h.install_dependencies(patch)
        h.file_inputs[0 if which == "instance" else 1] = (
            "bad-i" if which == "instance" else "bad-c", exc
        )
        with pytest.raises(OSError) as caught:
            _cli.main(["verify", "bad-i", "bad-c"])
        assert caught.value is exc
        h.conserved()
    assert h.calls["verify"] == h.calls["from_dict"] == 0
    assert h.streams[1].accesses == h.streams[2].accesses == 0
    expected = [("open", "bad-i")]
    if which == "certificate":
        expected += [("read", "bad-i"), ("close", "bad-i"), ("open", "bad-c")]
    assert h.events == expected


def test_invalid_instance_with_readable_certificate_reaches_only_checker(monkeypatch):
    h = _Harness("verify")
    h.input_bytes = b"invalid instance\n"
    exc = ValueError("independent checker rejects acquired input")
    h.faults["verify"] = exc
    with monkeypatch.context() as patch:
        h.install_io(patch, ("i", "c"))
        h.install_dependencies(patch)
        with pytest.raises(ValueError) as caught:
            _cli.main(["verify", "i", "c"])
        assert caught.value is exc
        h.conserved()
    assert h.calls["from_dict"] == 0 and h.calls["verify"] == 1
    assert h.events == [
        ("open", "i"), ("read", "i"), ("close", "i"),
        ("open", "c"), ("read", "c"), ("close", "c"), ("verify",),
    ]


def test_argv_is_not_retained_or_cached_between_calls(monkeypatch):
    argv = ["--help"]
    before = sum(item is vars(_cli) for item in gc.get_referrers(argv))
    h = _Harness("help")
    h.operands = ()
    _assert_success(h, _call(h, argv, monkeypatch), _TEXT["ROOT_HELP"])
    assert not any(value is argv for value in vars(_cli).values())
    assert sum(item is vars(_cli) for item in gc.get_referrers(argv)) == before
    argv[:] = ["verify", "-", "-"]
    second = _Harness("usage")
    second.operands = ()
    _assert_success(second, _call(second, argv, monkeypatch), _TEXT["USAGE_ERROR"])
    assert argv == ["verify", "-", "-"]


def _attainment_and_optimum(ib, cb, graph):
    obj = _W.verify(ib, cb)
    expected = _F.global_reference(graph, "endpoints")
    assert obj["N"] * expected[1] == expected[0] * obj["D"]
    return obj


def test_all_400_qualified_graphs_both_real_selections_repeats_and_local_candidates(monkeypatch):
    assert len(_GRAPHS) == 400 and len({key for key, _ in _GRAPHS}) == 400
    assert _F.fingerprint(_GRAPHS) == (
        "776ed183b5cd778b9e43ce0da08a809149bf233ac1fd9d928c63159d0dde5566"
    )
    origins = Counter()
    h2_shapes = Counter()
    first_calls = repeated_calls = local_checks = comparisons = 0
    visited = []
    original_baseline, original_endpoint, original_evaluate = (
        _solver._baseline, _solver._endpoint, _solver._evaluate
    )
    for gid, graph in _GRAPHS:
        ib = _F.encode(graph)
        results = []
        visited.append(gid)
        for route in _ROUTES:
            local = []

            def capture(value, witness, origin, local=local):
                local.append((value, witness, origin))

            def baseline(*args, capture=capture):
                result = original_baseline(*args)
                capture(*result, "Baseline")
                return result

            def endpoint(instance, branch, result, capture=capture):
                answer = original_endpoint(instance, branch, result)
                capture(*answer, ("L0", "L1", "H0", "H1")[branch])
                return answer

            def evaluate(instance, witness, capture=capture):
                value = original_evaluate(instance, witness)
                if sys._getframe(1).f_code is _ORIGINAL_SOLVE.__code__:
                    capture(value, witness, "H2")
                return value

            def run_once(ib=ib, graph=graph, route=route):
                harness = _Harness("solve", route)
                harness.input_bytes = ib
                harness.expected_graph = graph
                harness.real_solve = True
                harness.operands = ("ordered-graph",)
                answer = _call(harness, ["solve", "ordered-graph", "--solver", route], monkeypatch)
                assert type(answer) is int and answer == 0
                assert harness.calls["solve"] == harness.calls["verify"] == 1
                assert harness.stdout.flushes == 1 and not harness.stderr.output
                raw = bytes(harness.stdout.output)
                parsed = _attainment_and_optimum(ib, raw, graph)
                actual = harness.returned_result.value
                assert (parsed["N"], parsed["D"]) == (actual.N, actual.D)
                return harness, raw, parsed

            with monkeypatch.context() as patch:
                patch.setattr(_solver, "_baseline", baseline)
                patch.setattr(_solver, "_endpoint", endpoint)
                patch.setattr(_solver, "_evaluate", evaluate)
                first_harness, first_bytes, first_obj = run_once()
            first_calls += 1
            _, repeated_bytes, _ = run_once()
            repeated_calls += 1
            assert first_bytes == repeated_bytes
            results.append(first_obj)
            for value, witness, origin in local:
                source_result = _solver.SolveResult(value, witness)
                source_object = _ORIGINAL_BUILD(first_harness.instance, source_result)
                cb = _ORIGINAL_SERIALIZE(first_harness.instance, source_object)
                parsed = _W.verify(ib, cb)
                assert (parsed["N"], parsed["D"]) == (value.N, value.D)
                verifier = _Harness("verify")
                verifier.input_bytes, verifier.certificate_bytes = ib, cb
                verifier.operands = ("i", "c")
                _assert_success(verifier, _call(verifier, ["verify", "i", "c"], monkeypatch), b"")
                local_checks += 1
                origins[origin] += 1
                if origin == "H2":
                    h2_shapes["one-edge" if len(parsed["y"]) == 1 else "split"] += 1
        assert results[0]["N"] * results[1]["D"] == results[1]["N"] * results[0]["D"]
        comparisons += 1
    assert visited == [key for key, _ in _GRAPHS]
    assert (first_calls, repeated_calls, local_checks, comparisons) == (800, 800, 4006, 400)
    assert origins == {"Baseline": 796, "L0": 616, "L1": 578, "H0": 720, "H1": 758, "H2": 538}
    assert h2_shapes == {"one-edge": 378, "split": 160}



def _project_name(path):
    relative = path.removesuffix(".py").replace("/", ".")
    return relative.removesuffix(".__init__")


def _export(tmp_path, restricted=False):
    root = tmp_path / "export"
    root.mkdir()
    paths = (
        ["exactfrac/__init__.py", "exactfrac/cli.py", "exactfrac_verify/__init__.py",
         "exactfrac_verify/check.py"]
        if restricted else [*_CLOSED_PATHS, "exactfrac/cli.py", "tests/test_cli.py"]
    )
    hashes = {}
    for relative in paths:
        raw = (_ROOT / relative).read_bytes()
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(raw)
        hashes[relative] = _sha(raw)
    return root, hashes


def _fresh(source, payload, root, limit, seed):
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("PYTHON") and not key.startswith("PYTEST")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED=seed, PYTEST_DISABLE_PLUGIN_AUTOLOAD="1")
    data = dict(payload, root=str(root), limit=limit, seed=seed)
    answer = subprocess.run(
        [sys.executable, "-B", "-s", "-X", "int_max_str_digits=" + str(limit), "-c", source],
        input=json.dumps(data).encode(), capture_output=True, cwd=root, env=env,
        check=False, timeout=300,
    )
    assert answer.returncode == 0, answer.stderr.decode("utf-8", "replace")
    assert not answer.stderr
    return json.loads(answer.stdout)


def _wire_payload():
    return [(key, ib.hex(), cb.hex(), good) for key, ib, cb, good, _ in _WIRE]


@pytest.mark.parametrize("limit", [4300, 640])
@pytest.mark.parametrize("seed", ["1", "73"])
def test_fresh_independent_reference_has_no_project_dependencies(limit, seed, tmp_path):
    answer = _fresh(
        _REFERENCE_WORKER,
        {"source": _REFERENCE_SOURCES["independent_wire"],
         "source_sha256": _REFERENCE_HASHES["independent_wire"], "pairs": _wire_payload()},
        tmp_path, limit, seed,
    )
    assert answer == {
        "accepted": 64, "rejected": 455, "limit": limit, "seed": seed,
        "project_imports": [], "forbidden_import_attempts": [], "settings_unchanged": True,
    }


@pytest.mark.parametrize("limit", [4300, 640])
@pytest.mark.parametrize("seed", ["1", "73"])
@pytest.mark.parametrize("mode", ["help-usage", "verify"])
def test_fresh_cli_dependency_isolation_physically_without_producers(mode, limit, seed, tmp_path):
    root, hashes = _export(tmp_path, restricted=True)
    assert not (root / "exactfrac/instance.py").exists()
    assert not (root / "exactfrac/solve.py").exists()
    assert not (root / "exactfrac/certificate.py").exists()
    cases = []
    for key, tokens, kind, _, _, out, err, status, _ in _TABLES["U19_ARGV"]:
        if kind == "usage" or kind.endswith("_HELP"):
            cases.append((key, list(tokens), "usage" if kind == "usage" else "help",
                          _TEXT[out].hex(), _TEXT[err].hex(), status))
    payload = {"mode": mode, "files": hashes, "cases": cases, "pairs": _wire_payload()}
    answer = _fresh(_CLI_WORKER, payload, root, limit, seed)
    assert answer["settings_unchanged"] and answer["forbidden_import_attempts"] == []
    assert answer["calls"] == (519 if mode == "verify" else 64)
    assert answer["solver_calls"] == 0
    if mode == "verify":
        assert (answer["accepted"], answer["rejected"]) == (64, 455)
        assert set(answer["project_imports"]) == {
            "exactfrac", "exactfrac.cli", "exactfrac_verify", "exactfrac_verify.check",
        }
    else:
        assert set(answer["project_imports"]) == {"exactfrac", "exactfrac.cli"}
    assert {name: _sha((root / name).read_bytes()) for name in hashes} == hashes


@pytest.mark.parametrize("limit", [4300, 640])
@pytest.mark.parametrize("seed", ["1", "73"])
def test_fresh_huge_solve_both_selections_and_literal_pair_observation(limit, seed, tmp_path):
    root, hashes = _export(tmp_path)
    instances = [(key, _F.encode(graph).hex()) for key, graph in _GRAPHS
                 if key.startswith("U17_INPUTS/BIG-")]
    assert len(instances) == 4
    for key, _, parts, _, _, category, _, _ in _TABLES["U19_INSTANCE_SYNTAX"]:
        raw = _U19.bytes_recipe(parts)
        if category == "valid" and len(raw) > 4300:
            instances.append(("encoding/" + key, raw.hex()))
    payload = {
        "mode": "solve", "files": hashes, "instances": instances,
        "project_names": [_project_name(p) for p in hashes
                          if p.endswith(".py")
                          and p.split("/")[0] in {"exactfrac", "exactfrac_verify"}],
    }
    result = _fresh(_CLI_WORKER, payload, root, limit, seed)
    assert result["calls"] == result["solver_calls"] == 4 * len(instances)
    assert len(result["outputs"]) == 2 * len(instances)
    assert result["settings_unchanged"] and result["forbidden_import_attempts"] == []
    inputs = {key: bytes.fromhex(raw) for key, raw in instances}
    observed = {}
    for key, route, wire, raw_pair in result["outputs"]:
        ib, cb = inputs[key], bytes.fromhex(wire)
        obj = _attainment_and_optimum(ib, cb, _W.parse_instance(ib))
        assert (obj["N"], obj["D"]) == tuple(int(token, 16) for token in raw_pair)
        observed[key, route] = obj
    for key in inputs:
        left, right = observed[key, "Standard"], observed[key, "Accelerated"]
        assert left["N"] * right["D"] == right["N"] * left["D"]
    assert {name: _sha((root / name).read_bytes()) for name in hashes} == hashes


_MODULE_CASES = [
    ("root-help", ["--help"], None, "ROOT_HELP", 0),
    ("root-short-help", ["-h"], None, "ROOT_HELP", 0),
    ("solve-help", ["solve", "--help"], None, "SOLVE_HELP", 0),
    ("solve-short-help", ["solve", "-h"], None, "SOLVE_HELP", 0),
    ("verify-help", ["verify", "--help"], None, "VERIFY_HELP", 0),
    ("verify-short-help", ["verify", "-h"], None, "VERIFY_HELP", 0),
    ("empty-usage", [], None, "USAGE_ERROR", 2),
    ("two-stdin-usage", ["verify", "-", "-"], None, "USAGE_ERROR", 2),
    ("help-extra-usage", ["solve", "--help", "i"], None, "USAGE_ERROR", 2),
    ("verify-files", ["verify", "i", "c"], None, "SILENT", 0),
    ("verify-stdin-instance", ["verify", "-", "c"], "instance", "SILENT", 0),
    ("verify-stdin-certificate", ["verify", "i", "-"], "certificate", "SILENT", 0),
    ("verify-rejection", ["verify", "i", "bad-c"], None, "FAIL", None),
    ("solve-syntax-error", ["solve", "bad-i"], None, "FAIL", None),
    *[(route + "-" + operand, ["solve", "--solver", route, operand],
       "instance" if operand == "-" else None, "SOLVED", 0)
      for route in _ROUTES for operand in ("i", "-")],
]


@pytest.mark.parametrize("case", _MODULE_CASES, ids=[r[0] for r in _MODULE_CASES])
def test_real_module_entry_binary_files_stdin_and_process_status(case, tmp_path):
    _, argv, stdin_kind, expected, status = case
    root, hashes = _export(tmp_path)
    files = {"i": _DEFAULT_INPUT, "c": _DEFAULT_CERT, "bad-i": b"malformed JSON\n",
             "bad-c": b"malformed certificate\n"}
    for name, raw in files.items():
        (root / name).write_bytes(raw)
    payload = {None: b"", "instance": _DEFAULT_INPUT, "certificate": _DEFAULT_CERT}[stdin_kind]
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("PYTHON") and not key.startswith("PYTEST")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="73")
    before = {
        str(p.relative_to(root)): _sha(p.read_bytes()) for p in root.rglob("*") if p.is_file()
    }
    answer = subprocess.run(
        [sys.executable, "-B", "-s", "-m", "exactfrac.cli", *argv], input=payload,
        capture_output=True, cwd=root, env=env, check=False, timeout=180,
    )
    if status is None:
        assert answer.returncode != 0 and answer.stdout == b""
    else:
        assert answer.returncode == status
        if expected == "SOLVED":
            _attainment_and_optimum(_DEFAULT_INPUT, answer.stdout, _DEFAULT_GRAPH)
            assert answer.stderr == b""
        elif status == 2:
            assert answer.stdout == b"" and answer.stderr == _TEXT[expected]
        else:
            assert answer.stdout == _TEXT[expected] and answer.stderr == b""
    after = {str(p.relative_to(root)): _sha(p.read_bytes()) for p in root.rglob("*") if p.is_file()}
    assert after == before
    assert {name: _sha((root / name).read_bytes()) for name in hashes} == hashes


def _require_prefix(raw, length, digest):
    assert len(raw) >= length
    assert _sha(raw[:length]) == digest


@pytest.mark.parametrize("length,digest", _PREFIX_PINS)
def test_historical_and_unit19_catalogue_prefixes_are_length_and_hash_guarded(length, digest):
    raw = _CATALOGUE.read_bytes()
    _require_prefix(raw, length, digest)
    protected = raw[:length]
    _require_prefix(protected, length, digest)
    _require_prefix(protected + b"future authorized appendix", length, digest)
    bad = [b"", protected[:-1]]
    for position in (0, length // 2, length - 1):
        changed = bytearray(protected)
        changed[position] ^= 1
        bad.append(bytes(changed))
    for corrupted in bad:
        with pytest.raises(AssertionError):
            _require_prefix(corrupted, length, digest)


def test_registered_fixture_tables_and_qualified_censuses():
    assert tuple(_TABLES["U19_FINGERPRINTS"]) == _TABLE_PINS
    for name, count, digest in _TABLE_PINS:
        assert len(_TABLES[name]) == count and _F.fingerprint(_TABLES[name]) == digest
    for key, parts, size, digest in _TABLES["U19_TEXT"]:
        raw = _U19.bytes_recipe(parts)
        assert len(raw) == size and _sha(raw) == digest
        assert raw == _TEXT[key]
    assert len(_GRAPHS) == 400 and len(_LITERALS) == 41 and len(_WIRE) == 519
    assert Counter(good for _, _, _, good, _ in _WIRE) == {True: 64, False: 455}
    assert _F.fingerprint(_GRAPHS) == (
        "776ed183b5cd778b9e43ce0da08a809149bf233ac1fd9d928c63159d0dde5566"
    )
    wire_rows = [(k, ib.hex(), cb.hex(), good, why) for k, ib, cb, good, why in _WIRE]
    assert _F.fingerprint(wire_rows) == (
        "0a080728c39a3de3a0c76ac620967ea1cc00b035578d5cd9f0570e893b760bc9"
    )
    for ib, cb, row in _LITERALS.values():
        parsed = _W.verify(ib, cb)
        assert (parsed["N"], parsed["D"]) == (_F.number(row[5]), _F.number(row[6]))


def test_cli_source_dependency_and_process_setting_boundary():
    source = _CLI_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert not any(isinstance(n, (ast.Global, ast.Nonlocal)) for n in ast.walk(tree))
    allowed = {
        "sys", "json", "__future__", "exactfrac.instance", "exactfrac.solve",
        "exactfrac.certificate", "exactfrac_verify.check",
    }
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    imported_aliases = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imported_aliases.update((a.asname or a.name, a.name) for a in node.names)
    forbidden_calls = {
        "eval", "exec", "compile", "__import__", "float", "set_int_max_str_digits",
        "setrecursionlimit", "chdir", "_exit", "from_records", "solve_with_telemetry", "gcd",
    }
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            modules = (
                [alias.name for alias in node.names]
                if isinstance(node, ast.Import) else [node.module]
            )
            if isinstance(node, ast.ImportFrom) and node.level:
                assert node.level == 1 and node.module in {"instance", "solve", "certificate"}
                modules = ["exactfrac." + node.module]
            assert all(module in allowed for module in modules)
            if any(module.startswith("exactfrac") for module in modules):
                ancestor = parents.get(node)
                while ancestor is not None and not isinstance(
                    ancestor, (ast.FunctionDef, ast.AsyncFunctionDef)
                ):
                    ancestor = parents.get(ancestor)
                assert isinstance(ancestor, ast.FunctionDef), "Command dependency imported eagerly"
            if isinstance(node, ast.ImportFrom):
                assert not any(
                    alias.name.startswith("_") or alias.name == "*" for alias in node.names
                )
        if isinstance(node, ast.Call):
            target = node.func
            name = (
                target.id if isinstance(target, ast.Name)
                else target.attr if isinstance(target, ast.Attribute) else None
            )
            assert name not in forbidden_calls
        if isinstance(node, ast.ExceptHandler):
            assert node.type is not None
            names = {n.id for n in ast.walk(node.type) if isinstance(n, ast.Name)}
            names |= {n.attr for n in ast.walk(node.type) if isinstance(n, ast.Attribute)}
            assert {imported_aliases.get(name, name) for name in names} <= {
                "UnicodeDecodeError", "json", "JSONDecodeError"
            }
        if isinstance(node, ast.Constant):
            assert not isinstance(node.value, float)
    for source_text in _REFERENCE_SOURCES.values():
        assert source_text not in source
    assert _REFERENCE_HASHES["independent_wire"] != _sha(source.encode())
    # Closed source/tests/configuration are static here; documentation can later
    # receive separately authorized appendices without a permanent absence guard.
    for relative, digest in _FROZEN_SOURCE_HASHES.items():
        assert _sha((_ROOT / relative).read_bytes()) == digest, relative
    assert _sha(_CLI_PATH.read_bytes()) == _sha(source.encode())


@pytest.mark.parametrize("command", ["help", "usage"])
@pytest.mark.parametrize(
    "row", [r for r in _TABLES["U19_PROMISE_FAULTS"] if r[1] in {"write return", "flush return"}],
    ids=[r[0] for r in _TABLES["U19_PROMISE_FAULTS"] if r[1] in {"write return", "flush return"}],
)
def test_help_and_usage_enforce_all_binary_return_promises(command, row, monkeypatch):
    _, site, descriptor, *_ = row
    h = _Harness(command)
    writer = h.stdout if command == "help" else h.stderr
    if site == "write return":
        writer.fault_count = _write_fault(descriptor)
    else:
        writer.fault_flush = _bad_normal(h, site, descriptor)
    with monkeypatch.context() as patch:
        h.install_io(patch)
        h.install_dependencies(patch)
        with pytest.raises(RuntimeError) as caught:
            _cli.main(["--help"] if command == "help" else [])
        assert type(caught.value) is RuntimeError
        h.conserved()
    assert len(writer.writes) == 1
    assert writer.flushes == (1 if site == "flush return" else 0)
    assert not h.readers and not h.stdin.reads


@pytest.mark.parametrize("position", [0, 1])
@pytest.mark.parametrize("from_stdin", [False, True])
@pytest.mark.parametrize(
    "row", [r for r in _TABLES["U19_PROMISE_FAULTS"] if r[1] == "reader"],
    ids=[r[0] for r in _TABLES["U19_PROMISE_FAULTS"] if r[1] == "reader"],
)
def test_verify_checks_each_reader_byte_promise_before_checker(
    row, position, from_stdin, monkeypatch
):
    h = _Harness("verify")
    bad = _bad_normal(h, "reader", row[2])
    operands = ["i", "c"]
    if from_stdin:
        operands[position] = "-"
    target = "stdin" if from_stdin else operands[position]
    original_read = _Reader.read

    def read(reader, size=-1):
        result = original_read(reader, size)
        return bad if reader.label == target else result

    with monkeypatch.context() as patch:
        h.install_io(patch, tuple(operands))
        h.install_dependencies(patch)
        patch.setattr(_Reader, "read", read)
        with pytest.raises(RuntimeError) as caught:
            _cli.main(["verify", *operands])
        assert type(caught.value) is RuntimeError
        h.conserved()
    assert h.calls["verify"] == 0
    assert h.streams[1].accesses == h.streams[2].accesses == 0
    if position == 0:
        assert h.file_inputs == [(operands[1], h.certificate_bytes)]
