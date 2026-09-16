"""Syntax-only Unit 16 source conservation and exact legacy-test adapter checks.

Immutable source strings are parsed, never imported, compiled, or executed.
Human catalogue tables govern the site inventory and comparison-fixture identity.
Only the seven named observation forms may be erased from mathematical source.
"""
from __future__ import annotations

import ast
import hashlib
import json
from collections import Counter, deque
from itertools import pairwise
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = "tests/fixtures/unit16_legacy_sources.json"
REFERENCE_SHA = "e81ba1aac48412d7b9e85bb493d1edef1f98e6788d3ef67070b4a9ae21993136"
PRIMITIVES = (
    "_tap_int", "_tap_pair", "_tap_numerator", "_observe_ints",
    "_observe_pair_values", "_record_prepared_sizes", "_branch_scope",
)
TAPS = PRIMITIVES[:3]
EVENTS = PRIMITIVES[3:6]
FINGERPRINT_TABLE_SHA = '4f6fa2c78b80915d5ef096a59fc130b42ec4887e8c19e518216634bf843cf6d5'
ADAPTER_RECIPES = [{'path': 'tests/test_instance.py',
  'function': 'test_instance_imports_only_standard_library_modules',
  'original_function_sha256': 'b65f4021f0ae19a7e02f77289364be575db6c33e1863044ca144c1648cc25a25',
  'replacements': [['assert not any(name.startswith(".") for name in imported)',
                    'assert not any(name.startswith(".") and name != "._telemetry" for name in '
                    'imported)'],
                   ['set(sys.stdlib_module_names) | {"__future__"}',
                    'set(sys.stdlib_module_names) | {"__future__", "_telemetry"}']]},
 {'path': 'tests/test_shore.py',
  'function': 'test_oracle_022_source_is_graph_independent_and_stdlib_only',
  'original_function_sha256': '7f5aeebf7679a52641c1842a3cb3b2320f8a24289d113ce43415688d492960e3',
  'replacements': [['assert not any(name.startswith(".") for name in imported)',
                    'assert not any(name.startswith(".") and name != "._telemetry" for name in '
                    'imported)'],
                   ['set(sys.stdlib_module_names) | {"__future__"}',
                    'set(sys.stdlib_module_names) | {"__future__", "_telemetry"}']]},
 {'path': 'tests/test_families.py',
  'function': 'test_oracle_029_static_import_and_exactness_boundary',
  'original_function_sha256': '887938181b6cc6e71c1d850330075ddb45bd160228889fafeb892ef79500bf09',
  'replacements': [['allowed_relative = {".instance", ".shore"}',
                    'allowed_relative = {".instance", ".shore", "._telemetry"}'],
                   ['allowed_absolute = {"exactfrac.instance", "exactfrac.shore"}',
                    'allowed_absolute = {"exactfrac.instance", "exactfrac.shore", '
                    '"exactfrac._telemetry"}']]},
 {'path': 'tests/test_witness.py',
  'function': 'test_source_exactness_import_boundary_and_no_numeric_shortcuts',
  'original_function_sha256': '6207d16b559fa7802da47ee104fda40609ab168d5e466f5b0510c5ffcba423a0',
  'replacements': [['allowed_imports = {"__future__", "dataclasses", "instance", "shore"}',
                    'allowed_imports = {"__future__", "dataclasses", "instance", "shore", '
                    '"_telemetry"}']]},
 {'path': 'tests/test_rational.py',
  'function': 'test_rp11_fresh_process_import_isolation_and_package_root',
  'original_function_sha256': '6a8342b3a486a62144a87a432db473d2609c08587a9764dbec79145097fdded8',
  'replacements': [['assert lines[1].split("|") == ["exactfrac", "exactfrac.rational"]',
                    'assert lines[1].split("|") in (\n'
                    '        ["exactfrac", "exactfrac.rational"],\n'
                    '        ["exactfrac", "exactfrac._telemetry", "exactfrac.rational"],\n'
                    '    )']]},
 {'path': 'tests/test_rational.py',
  'function': 'test_rp11_source_exactness_and_dependency_isolation',
  'original_function_sha256': '61e0b8ce3400ae42ecab739fd77928564a61429deec754a3d03547c2509c9396',
  'replacements': [['assert allowed_future, ast.unparse(node)',
                    (
                        'assert allowed_future or (\n                node.level ='
                        '= 1 and node.module == "_telemetry"\n                and'
                        ' {alias.name for alias in node.names} <= {\n            '
                        '        "_tap_int", "_tap_pair", "_tap_numerator", "_ob'
                        'serve_ints",\n                    "_observe_pair_values"'
                        ', "_record_prepared_sizes", "_branch_scope",\n          '
                        '      }\n                and all(alias.asname is None fo'
                        'r alias in node.names)\n            ), ast.unparse(node)'
                    )]]},
 {'path': 'tests/test_sign_routing.py',
  'function': 'test_fresh_process_import_isolation_and_export_free_package_root',
  'original_function_sha256': '9fd9812e84f93301e92cbac489b97484ee674c1493ddee3af8a1b411fb0781b1',
  'replacements': [['assert tuple(sorted(origins)) == (\n'
                    '        "exactfrac", "exactfrac.instance", "exactfrac.rational", '
                    '"exactfrac.sign_routing",\n'
                    '    )',
                    'assert tuple(sorted(origins)) in (\n'
                    '        ("exactfrac", "exactfrac.instance", "exactfrac.rational", '
                    '"exactfrac.sign_routing"),\n'
                    '        ("exactfrac", "exactfrac._telemetry", "exactfrac.instance",\n'
                    '         "exactfrac.rational", "exactfrac.sign_routing"),\n'
                    '    )']]},
 {'path': 'tests/test_sign_routing.py',
  'function': '_check_source',
  'original_function_sha256': '3d36e00566a60c091352ccdc93541293215506f6b5ef4f3971a9614c6b8c2fec',
  'replacements': [['allowed_from = {',
                    'allowed_from = {\n'
                    '        (1, "_telemetry"): {"_tap_int", "_tap_pair", "_tap_numerator", '
                    '"_observe_ints",\n'
                    '                       "_observe_pair_values", "_record_prepared_sizes", '
                    '"_branch_scope"},']]},
 {'path': 'tests/test_parity_cut.py',
  'function': '_source_violations',
  'original_function_sha256': '38e890706f438df6cc9de99edc9a0874a5afa4a38374f420967d0e465aff978a',
  'replacements': [['allowed = {"__future__":',
                    'allowed = {"_telemetry": {"_tap_int", "_tap_pair", "_tap_numerator", '
                    '"_observe_ints",\n'
                    '                       "_observe_pair_values", "_record_prepared_sizes", '
                    '"_branch_scope"},\n'
                    '               "__future__":']]},
 {'path': 'tests/test_parity_cut.py',
  'function': 'test_fresh_process_import_isolation',
  'original_function_sha256': '63b521aa47fa8ec81fe7a97e40dc3412057e34dc62c190839aa0dc236e2886ba',
  'replacements': [['allowed = {"exactfrac",', (
                        'allowed = {"exactfrac._telemetry",\n               "exac'
                        'tfrac",'
                    )]]},
 {'path': 'tests/test_oracle.py',
  'function': 'test_imports_in_a_fresh_process_resolve_only_closed_project_layers',
  'original_function_sha256': '12e538b32393f47ad675bdf87839d65ac7b5f96099b5e9470c271da15f072113',
  'replacements': [['allowed = {', (
                        'allowed = {"exactfrac._telemetry",\n           '
                    )]]},
 {'path': 'tests/test_oracle.py',
  'function': 'test_production_source_imports_exact_arithmetic_and_no_side_effect_paths',
  'original_function_sha256': 'd5934088546510b87b3ff3759d515d33580e7a0a2367fe4b5b27a73fbc0e7a27',
  'replacements': [['whitelist = {',
                    'whitelist = {\n'
                    '        "_telemetry": {"_tap_int", "_tap_pair", "_tap_numerator", '
                    '"_observe_ints",\n'
                    '                       "_observe_pair_values", "_record_prepared_sizes", '
                    '"_branch_scope"},']]},
 {'path': 'tests/test_branch.py',
  'function': 'test_fresh_process_imports_resolve_to_only_permitted_project_layers',
  'original_function_sha256': 'c76a34e4c884b8bfee4f0650e0c7eec12480f74f15c08a1dd5f7d2444308fbb5',
  'replacements': [['allowed = {', 'allowed = {"exactfrac._telemetry",']]},
 {'path': 'tests/test_branch_accelerated.py',
  'function': 'test_five_closed_definitions_and_compatibility_bytes_are_preserved',
  'original_function_sha256': 'f73497b5b4adc23fd142a899afd2f1a1a52b6473c2fef115762e29ba53a1d85a',
  'replacements': [['assert '
                    "(hashlib.sha256(Path(__file__).with_name('test_branch.py').read_bytes()).hexdigest(\n"
                    '        ) == _COMPATIBILITY_SHA256)',
                    'from _telemetry_source_audit import assert_test_adaptation, legacy_bytes\n'
                    '\n'
                    '    assert (hashlib.sha256(legacy_bytes("tests/test_branch.py")).hexdigest(\n'
                    '        ) == _COMPATIBILITY_SHA256)\n'
                    '    assert_test_adaptation("tests/test_branch.py")']]},
 {'path': 'tests/test_branch_accelerated.py',
  'function': 'test_fresh_process_combined_imports_resolve_only_to_candidate_tree',
  'original_function_sha256': 'ea98d0da3f45366cb3b82d32b14ce22c9180d648a003f4997c4db9d1efb94ba6',
  'replacements': [["'\\nimport importlib, json, pathlib, sys\\nroot = pathlib.Path(sys.ar'\n"
                    "        'gv[1]).resolve()\\nsys.path.insert(0, str(root))\\nbefore = "
                    "set(sys.'\n"
                    "        'modules)\\nmodule = "
                    'importlib.import_module("exactfrac.branch")\\nas\'\n'
                    '        \'sert module.__all__ == (\\n    "AcceleratedBranchStats", '
                    '"BranchRes\'\n'
                    '        \'ult", "StandardBranchStats",\\n    "solve_branch_accelerated", '
                    '"sol\'\n'
                    '        \'ve_branch_standard",\\n)\\nallowed = {"exactfrac", '
                    '"exactfrac.branch\'\n'
                    '        \'", "exactfrac.oracle", "exactfrac.rational",\\n           '
                    '"exactfra\'\n'
                    '        \'c.instance", "exactfrac.families", "exactfrac.shore", '
                    '"exactfrac.w\'\n'
                    '        \'itness",\\n           "exactfrac.flow", "exactfrac.sign_routing", '
                    '"\'\n'
                    '        \'exactfrac.parity_cut"}\\norigins = {}\\nfor name in '
                    "sorted(set(sys.m'\n"
                    '        \'odules) - before):\\n    if name.startswith(("exactfrac", '
                    '"tests"))\'\n'
                    "        ':\\n        assert name in allowed, name\\n        path = "
                    "pathlib.Pa'\n"
                    "        'th(sys.modules[name].__file__).resolve()\\n        expected = root "
                    "'\n"
                    '        \'/ ("exactfrac/__init__.py" if name == "exactfrac" else '
                    "name.replac'\n"
                    '        \'e(".", "/") + ".py")\\n        assert path == expected, (name, '
                    "path'\n"
                    "        ')\\n        origins[name] = str(path.relative_to(root))\\nassert "
                    "ori'\n"
                    '        \'gins["exactfrac.branch"] == "exactfrac/branch.py"\\nassert not '
                    "geta'\n"
                    '        \'ttr(sys.modules["exactfrac"], "__all__", '
                    "())\\nprint(json.dumps(ori'\n"
                    "        'gins, sort_keys=True))\\n'",
                    "'\\nimport importlib, json, pathlib, sys\\nroot = pathlib.Path(sys.ar'\n"
                    "        'gv[1]).resolve()\\nsys.path.insert(0, str(root))\\nbefore = "
                    "set(sys.'\n"
                    "        'modules)\\nmodule = "
                    'importlib.import_module("exactfrac.branch")\\nas\'\n'
                    '        \'sert module.__all__ == (\\n    "AcceleratedBranchStats", '
                    '"BranchRes\'\n'
                    '        \'ult", "StandardBranchStats",\\n    "solve_branch_accelerated", '
                    '"sol\'\n'
                    '        \'ve_branch_standard",\\n)\\nallowed = {"exactfrac._telemetry", '
                    '"exactfrac", "exactfrac.branch\'\n'
                    '        \'", "exactfrac.oracle", "exactfrac.rational",\\n           '
                    '"exactfra\'\n'
                    '        \'c.instance", "exactfrac.families", "exactfrac.shore", '
                    '"exactfrac.w\'\n'
                    '        \'itness",\\n           "exactfrac.flow", "exactfrac.sign_routing", '
                    '"\'\n'
                    '        \'exactfrac.parity_cut"}\\norigins = {}\\nfor name in '
                    "sorted(set(sys.m'\n"
                    '        \'odules) - before):\\n    if name.startswith(("exactfrac", '
                    '"tests"))\'\n'
                    "        ':\\n        assert name in allowed, name\\n        path = "
                    "pathlib.Pa'\n"
                    "        'th(sys.modules[name].__file__).resolve()\\n        expected = root "
                    "'\n"
                    '        \'/ ("exactfrac/__init__.py" if name == "exactfrac" else '
                    "name.replac'\n"
                    '        \'e(".", "/") + ".py")\\n        assert path == expected, (name, '
                    "path'\n"
                    "        ')\\n        origins[name] = str(path.relative_to(root))\\nassert "
                    "ori'\n"
                    '        \'gins["exactfrac.branch"] == "exactfrac/branch.py"\\nassert not '
                    "geta'\n"
                    '        \'ttr(sys.modules["exactfrac"], "__all__", '
                    "())\\nprint(json.dumps(ori'\n"
                    "        'gins, sort_keys=True))\\n'"]]},
 {'path': 'tests/test_solve.py',
  'function': 'test_gl19_direct_import_exactness_and_compact_source_controls',
  'original_function_sha256': '38eb5568e4a9691b7a85e3e2f419fa9fc03611daaabf883722587cfb49ca67e8',
  'replacements': [['allowed = {',
                    'allowed = {\n'
                    '        "_telemetry": {"_tap_int", "_tap_pair", "_tap_numerator", '
                    '"_observe_ints",\n'
                    '                       "_observe_pair_values", "_record_prepared_sizes", '
                    '"_branch_scope"},']]},
 {'path': 'tests/test_solve.py',
  'function': 'test_gl19_fresh_process_direct_import_isolation',
  'original_function_sha256': '91d6ef0c0c280aea65da03a1978c3356d776bfa7ee04eab6b5f942022f23964c',
  'replacements': [['allowed = {"__future__",', (
                        'allowed = {"_telemetry",\n               "__future__",'
                    )]]}]


# Fixed source universe and typed exclusions from the committed correction rule.
INVENTORY_MODULES = (
    "instance", "shore", "families", "witness", "rational", "sign_routing",
    "parity_cut", "flow", "oracle", "solve", "branch",
)
SIGNATURE_OWNERS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)
INVENTORY_DEFINITIONS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
INVENTORY_METADATA = frozenset((
    "annotation", "returns", "type_comment", "decorator_list", "type_params",
))
CORRECTION_FINGERPRINT_TABLE_SHA = (
    "480303c794eff0900dd52fccdd66d0b82806b178e66e396ce886067d60d39ee0"
)


def need(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(node: ast.AST) -> str:
    def normalize(value):
        if isinstance(value, ast.AST):
            return [type(value).__name__, [[k, normalize(v)] for k, v in ast.iter_fields(value)
                    if not (k == "type_params" and v == [])]]
        if isinstance(value, list):
            return [normalize(v) for v in value]
        if value is Ellipsis:
            return ["singleton", "Ellipsis"]
        if isinstance(value, bytes):
            return ["bytes", value.hex()]
        if isinstance(value, complex):
            return ["complex", repr(value)]
        return value
    return json.dumps(normalize(node), ensure_ascii=True, separators=(",", ":"))


def row_digest(rows: list) -> str:
    data = b"".join((json.dumps(row, separators=(",", ":"), ensure_ascii=True) + "\n").encode()
                    for row in rows)
    return digest(data)


def tables_from(text: str, prefix: str = "U16_") -> dict:
    tables = {}
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not line.startswith("### Fixture table: " + prefix):
            continue
        name = line.split(": ", 1)[1]
        need(name not in tables, "duplicate human fixture table " + name)
        j = i + 1
        while j < len(lines) and not lines[j].startswith("| "):
            j += 1
        need(j + 1 < len(lines), "missing table header " + name)
        j += 2
        rows = []
        while j < len(lines) and lines[j].startswith("| "):
            parts = lines[j][1:-1].split(" | ")
            cells = []
            for part in parts:
                part = part.strip()
                need(part.startswith("`") and part.endswith("`"), "nonliteral cell " + name)
                cells.append(
                    ast.literal_eval(part[1:-1].replace("&#124;", "|").replace("&#96;", "`"))
                )
            rows.append(cells)
            j += 1
        tables[name] = rows
    return tables


def load_tables(root: Path = ROOT) -> dict:
    text = (root / "docs/ORACLE_CATALOG.md").read_text(encoding="utf-8")
    tables = tables_from(text)
    need(len(tables) == 35, "incomplete historical Unit 16 table set")
    expected = {r[0]: (r[1], r[2]) for r in tables["U16_FINGERPRINTS"]}
    need(set(expected) == set(tables) - {"U16_FINGERPRINTS"}, "fingerprint coverage")
    for name, rows in tables.items():
        if name != "U16_FINGERPRINTS":
            need((len(rows), row_digest(rows)) == expected[name], "changed fixture " + name)
    need(row_digest(tables["U16_FINGERPRINTS"]) == FINGERPRINT_TABLE_SHA,
         "fingerprint table differs from committed oracle")
    correction = tables_from(text, "U16MC_")
    need(set(correction) == {
        "U16MC_EFFECTIVE_COUNTS", "U16MC_FINGERPRINTS", "U16MC_ITERATOR_ADDITIONS",
        "U16MC_RULE_FIXTURES", "U16MC_SCALAR_ADDITIONS", "U16MC_SOURCE_PINS",
    }, "incomplete committed manifest-correction table set")
    expected = {r[0]: (r[1], r[2]) for r in correction["U16MC_FINGERPRINTS"]}
    need(set(expected) == set(correction) - {"U16MC_FINGERPRINTS"},
         "correction fingerprint coverage")
    for name, rows in correction.items():
        if name != "U16MC_FINGERPRINTS":
            need((len(rows), row_digest(rows)) == expected[name], "changed correction " + name)
    need(row_digest(correction["U16MC_FINGERPRINTS"]) == CORRECTION_FINGERPRINT_TABLE_SHA,
         "correction fingerprint table differs from committed oracle")
    # Authenticate historical rows separately; select the append-only effective inventory.
    return {
        **tables, **correction,
        "U16_SCALAR_SITES": tables["U16_SCALAR_SITES"] + correction["U16MC_SCALAR_ADDITIONS"],
        "U16_ITERATOR_SITES": (
            tables["U16_ITERATOR_SITES"] + correction["U16MC_ITERATOR_ADDITIONS"]
        ),
    }


class _InventoryFunctions(ast.NodeVisitor):
    """Discover callable owners independently, including lexical nested definitions."""
    def __init__(self):
        self.qualifiers = []
        self.rows = []

    def visit_ClassDef(self, node):
        self.qualifiers.append(node.name)
        for statement in node.body:
            self.visit(statement)
        self.qualifiers.pop()

    def visit_FunctionDef(self, node):
        self.qualifiers.append(node.name)
        self.rows.append((".".join(self.qualifiers), node))
        for statement in node.body:
            self.visit(statement)
        self.qualifiers.pop()

    visit_AsyncFunctionDef = visit_FunctionDef


def _inventory_occurrences(function):
    """Enumerate the unpruned AST, retaining ownership/exclusion ancestry."""
    pending = deque((node, f"body[{i}]", ()) for i, node in enumerate(function.body))
    while pending:
        node, path, ancestors = pending.popleft()
        yield node, path, ancestors
        for field in node._fields:
            value = getattr(node, field)
            items = enumerate(value) if isinstance(value, list) else ((None, value),)
            for index, child in items:
                if isinstance(child, ast.AST):
                    edge = field if index is None else f"{field}[{index}]"
                    pending.append((child, path + "." + edge,
                                    (*ancestors, (node, field))))


def _inventory_inside_body(node, ancestors):
    """Typed signature exclusion; Call.args is NEVER excluded by its field name."""
    chain = (*(parent for parent, _ in ancestors), node)
    for part in chain:
        if isinstance(part, INVENTORY_DEFINITIONS):
            return False  # Owned by a separate callable, not its enclosing body.
        if (isinstance(part, ast.Expr) and isinstance(part.value, ast.Constant)
                and type(part.value.value) is str):
            return False
    for parent, field in ancestors:
        if field in INVENTORY_METADATA:
            return False
        if field == "args" and isinstance(parent, SIGNATURE_OWNERS):
            return False
    return True


def _inventory_candidate(node):
    if isinstance(node, (ast.BinOp, ast.UnaryOp, ast.AugAssign)):
        return True
    if not isinstance(node, ast.Call):
        return False
    function = node.func
    if isinstance(function, ast.Name):
        return function.id in ("len", "sum", "min", "max", "int", "abs")
    return isinstance(function, ast.Attribute) and function.attr in ("bit_count", "bit_length")


def inventory_from_sources(sources: dict[str, str]) -> dict:
    """Discover all candidate occurrences before seeing any manifest or row IDs.

    Source values are Python strings, not execution output. Synthetic rule controls
    may supply a single 'probe' module; callers authenticate the real module set.
    Classification as mathematical, diagnostic or outside does not prune discovery.
    """
    scalars, iterators, functions = [], [], []
    for module, source in sources.items():
        collector = _InventoryFunctions()
        collector.visit(ast.parse(source, filename=module + ".py", feature_version=(3, 11)))
        owners = collector.rows
        if len({name for name, _ in owners}) != len(owners):
            raise AssertionError("duplicate qualified function owner in " + module)
        for qual, function in owners:
            text = ast.get_source_segment(source, function)
            functions.append([module, qual, function.lineno, function.end_lineno,
                              hashlib.sha256(text.encode()).hexdigest()])
            for node, path, ancestors in _inventory_occurrences(function):
                if not _inventory_inside_body(node, ancestors):
                    continue
                if _inventory_candidate(node):
                    text = ast.get_source_segment(source, node) or ast.unparse(node)
                    scalars.append([module, qual, node.lineno, node.col_offset,
                                    node.end_lineno, node.end_col_offset, path,
                                    digest(canonical(node).encode()), " ".join(text.split())])
                if isinstance(node, (ast.For, ast.comprehension)):
                    iterator = node.iter
                    if (isinstance(iterator, ast.Call) and isinstance(iterator.func, ast.Name)
                            and iterator.func.id in ("range", "enumerate")):
                        iterators.append([module, qual, getattr(node, "lineno", iterator.lineno),
                                          path, ast.unparse(node.target), ast.unparse(iterator)])
    return {"functions": functions, "scalars": scalars, "iterators": iterators}


def _exact_multiset(actual, expected, label):
    left, right = Counter(map(tuple, actual)), Counter(map(tuple, expected))
    if any(number != 1 for number in left.values()):
        raise AssertionError("duplicate " + label + " identity")
    missing, extra = right - left, left - right
    if missing or extra:
        raise AssertionError(label + " coverage mismatch: missing " + repr(list(missing)[:3])
                           + "; extra " + repr(list(extra)[:3]))


def assert_inventory_complete(sources: dict[str, str], manifest: dict) -> dict:
    """Compare source discovery with supplied tables only AFTER enumeration."""
    found = inventory_from_sources(sources)
    scalar_rows = manifest["U16_SCALAR_SITES"]
    ids = [row[0] for row in scalar_rows]
    if len(ids) != len(set(ids)):
        raise AssertionError("duplicate scalar site ID")
    _exact_multiset(
        [row[:5] for row in manifest["U16_FUNCTIONS"]], found["functions"], "function",
    )
    _exact_multiset([row[1:10] for row in scalar_rows], found["scalars"], "scalar")
    _exact_multiset(
        [row[:6] for row in manifest["U16_ITERATOR_SITES"]], found["iterators"], "iterator",
    )
    return {"functions": len(found["functions"]), "scalar_sites": len(found["scalars"]),
            "iterator_sites": len(found["iterators"]), "enumeration_uses_manifest": False}


def inventory_sources(reference: dict, tables: dict) -> dict[str, str]:
    """Authenticate the fixed source universe; manifest rows do not choose modules."""
    sources = {}
    declared = {row[0]: row[1:] for row in tables["U16MC_SOURCE_PINS"]}
    paths = {"exactfrac/" + module + ".py" for module in INVENTORY_MODULES}
    need(set(declared) == paths, "corrected source-pin universe differs from authority")
    for module in INVENTORY_MODULES:
        name = "exactfrac/" + module + ".py"
        raw = reference["files"][name]["source"].encode()
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        need([digest(raw), blob] == declared[name], "original inventory source identity " + name)
        sources[module] = raw.decode()
    return sources


def load_reference(root: Path = ROOT) -> dict:
    data = (root / REFERENCE).read_bytes()
    need(digest(data) == REFERENCE_SHA, "immutable legacy JSON bytes")
    reference = json.loads(data)
    need(reference["format"] == "unit16-immutable-legacy-source-data-v1", "reference format")
    need(reference["source_commit"] == "bea6257153b760d009997a53c05003013aff3ef0",
         "reference authority commit")
    tables = load_tables(root)
    declared = {r[0]: r[1:] for r in tables["U16_LEGACY_REFERENCES"]}
    need(set(reference["files"]) == set(declared), "legacy file inventory")
    for name, record in reference["files"].items():
        raw = record["source"].encode()
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        need([digest(raw), blob, record["mode"], len(raw)] == declared[name],
             "legacy identity " + name)
        need(record["sha256"] == digest(raw) and record["blob"] == blob
             and record["bytes"] == len(raw), "legacy self-description " + name)
    return reference


def legacy_bytes(name: str, root: Path = ROOT) -> bytes:
    return load_reference(root)["files"][name]["source"].encode()


def expected_test(name: str, original: bytes, tables: dict) -> bytes:
    source = original.decode()
    functions = {n.name: n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef)}
    declared = {(r[0], r[1]): r for r in tables["U16_GUARD_ADAPTERS"]}
    lines = source.splitlines(keepends=True)
    edits = []
    for recipe in (r for r in ADAPTER_RECIPES if r["path"] == name):
        key = (name, recipe["function"])
        need(key in declared, "unregistered legacy-test adapter")
        node = functions[recipe["function"]]
        old = ast.get_source_segment(source, node)
        need(digest(old.encode()) == declared[key][4] == recipe["original_function_sha256"],
             "original guard bytes " + repr(key))
        new = old
        for before, after in recipe["replacements"]:
            need(new.count(before) == 1, "nonunique guard edit " + repr(key))
            new = new.replace(before, after)
        start = sum(map(len, lines[:node.lineno - 1])) + node.col_offset
        end = sum(map(len, lines[:node.end_lineno - 1])) + node.end_col_offset
        edits.append((start, end, new))
    for start, end, new in sorted(edits, reverse=True):
        source = source[:start] + new + source[end:]
    ast.parse(source)
    return source.encode()


def assert_test_adaptation(name: str, candidate: bytes | None = None, root: Path = ROOT) -> None:
    tables = load_tables(root)
    wanted = expected_test(name, legacy_bytes(name, root), tables)
    actual = (root / name).read_bytes() if candidate is None else candidate
    need(actual == wanted, "non-enumerated test edit: " + name)


def functions(tree: ast.AST, prefix: str = "") -> dict:
    result = {}
    for node in getattr(tree, "body", ()):
        if isinstance(node, ast.ClassDef):
            result.update(functions(node, prefix + node.name + "."))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result[prefix + node.name] = node
            result.update(functions(node, prefix + node.name + "."))
    return result


def at_path(node: ast.AST, path: str) -> ast.AST:
    for part in path.split("."):
        if "[" in part:
            field, index = part[:-1].split("[")
            node = getattr(node, field)[int(index)]
        else:
            node = getattr(node, part)
    return node


def pure_load(node: ast.AST, allow_length: bool = False) -> bool:
    if isinstance(node, ast.Name):
        return isinstance(node.ctx, ast.Load)
    if isinstance(node, ast.Constant):
        return type(node.value) is int
    if isinstance(node, ast.Attribute):
        return node.attr not in {"Q", "m", "d_q"} and pure_load(node.value)
    if isinstance(node, ast.Subscript):
        return pure_load(node.value) and pure_load(node.slice)
    if isinstance(node, (ast.Tuple, ast.List)):
        return all(pure_load(x) for x in node.elts)
    return bool(allow_length and isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name) and node.func.id == "len"
                and len(node.args) == 1 and not node.keywords and pure_load(node.args[0]))


class Eraser(ast.NodeTransformer):
    """Remove only audited identity observations, not arbitrary program statements."""

    def __init__(self, allowed_functions: set[str]) -> None:
        self.allowed_functions = allowed_functions
        self.observations = []
        self.pair_sites = []
        self.imports = set()
        self.current = ""

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        old = self.current
        self.current = node.name
        body = []
        # Observation hooks are permitted in bodies, not signatures or decorators.
        for statement in node.body:
            visited = self.visit(statement)
            if isinstance(visited, list):
                body.extend(visited)
            elif visited is not None:
                body.append(visited)
        node.body = body
        self.current = old
        return node

    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.AST | None:
        if node.module != "_telemetry":
            return node
        need(node.level == 1 and all(a.name in PRIMITIVES and a.asname is None for a in node.names),
             "unapproved observation import")
        self.imports.update(a.name for a in node.names)
        return None

    def visit_Call(self, node: ast.Call) -> ast.AST:
        self.generic_visit(node)
        name = node.func.id if isinstance(node.func, ast.Name) else None
        if name in TAPS:
            need(self.current in self.allowed_functions, "tap outside the measured call graph")
            need(name in self.imports, "tap without approved import")
            need(not node.keywords and len(node.args) == (2 if name == "_tap_numerator" else 1),
                 "tap argument shape")
            if name == "_tap_numerator":
                need(pure_load(node.args[1]), "extra denominator computation in tap")
            value = node.args[0]
            value._u16_tapped = True
            value._u16_tap_kinds = (*getattr(value, "_u16_tap_kinds", ()), name)
            if name == "_tap_numerator":
                value._u16_denominator = canonical(node.args[1])
            if name in {"_tap_pair", "_tap_numerator"}:
                self.pair_sites.append(self.current)
            return value
        need(name not in EVENTS and name != "_branch_scope", "mathematical read of recording event")
        return node

    def visit_Expr(self, node: ast.Expr) -> ast.AST | None:
        call = node.value
        name = (
            call.func.id
            if isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
            else None
        )
        if name in EVENTS:
            need(self.current in self.allowed_functions, "event outside the measured call graph")
            need(name in self.imports and not call.keywords, "unapproved observation statement")
            need(
                call.args
                and all(pure_load(a, name == "_record_prepared_sizes") for a in call.args),
                "extra evaluation inside observation statement",
            )
            if name == "_observe_pair_values":
                need(len(call.args) == 2, "pair observation arity")
                self.pair_sites.append(self.current)
            if name == "_record_prepared_sizes":
                need(self.current == "enumerate_atomic_families" and len(call.args) == 4,
                     "preparation observation placement or shape")
                need(
                    [ast.unparse(a) for a in call.args]
                    == ["len(d0)", "len(d1)", "len(d2)", "len(d3)"],
                    "preparation must record actual emitted cover lengths",
                )
            self.observations.append((self.current, name, call.args, node.lineno))
            return None
        return self.generic_visit(node)

    def visit_With(self, node: ast.With) -> list[ast.stmt]:
        need(len(node.items) == 1, "unruled scope wrapper")
        item = node.items[0]
        call = item.context_expr
        need(item.optional_vars is None and isinstance(call, ast.Call)
             and isinstance(call.func, ast.Name) and call.func.id == "_branch_scope"
             and call.func.id in self.imports and not call.keywords and len(call.args) == 1
             and isinstance(call.args[0], ast.Name) and call.args[0].id == "branch",
             "unapproved scope expression")
        need(self.current == "solve", "branch scope outside global branch loop")
        body = []
        for child in node.body:
            value = self.visit(child)
            if value is not None:
                need(isinstance(value, ast.stmt), "nested scope structure")
                value._u16_scope = "branch"
                body.append(value)
        return body


# Authorized alternative for exactly the two coefficient-generator D-ITER sites.
_COEFFICIENT_BOUND_PATHS = (
    "body[7].body[1].value.args[0].generators[0]",
    "body[7].orelse[0].value.args[0].generators[0]",
)


def _mark_coefficient_bound_statement(module: str, current: dict) -> None:
    """Mark only a same-body, immediate, exact and unreassigned bound observation.

    This mark is necessary, not sufficient: full original-program AST conservation
    and the registered iterator identity are also required before acceptance.
    No function, generator or mathematical source string is executed here.
    """
    if module != "sign_routing" or "branch_coefficients" not in current:
        return
    function = current["branch_coefficients"]
    condition = canonical(ast.parse("branch < 2", mode="eval").body)
    operand = canonical(ast.parse("instance.n", mode="eval").body)
    selections = [
        (i, node) for i, node in enumerate(function.body)
        if isinstance(node, ast.If) and canonical(node.test) == condition
    ]
    if len(selections) != 1:
        return
    position, selection = selections[0]
    # Reset a stale marker if this checker is used twice on the same parsed tree.
    selection._u16_preceding_coefficient_bound = False
    if position == 0:
        return
    preceding = function.body[position - 1]
    event = preceding.value if isinstance(preceding, ast.Expr) else None
    if not (
        isinstance(event, ast.Call) and isinstance(event.func, ast.Name)
        and event.func.id == "_observe_ints" and not event.keywords
        and len(event.args) == 1 and canonical(event.args[0]) == operand
    ):
        return
    # Immediate adjacency excludes an intervening store before the selection.
    # Inspect its branches too: no rebinding, attribute write or deletion of
    # instance may intervene before either bound is evaluated. Reject extra scopes;
    # the unchanged mathematical AST separately excludes mutating calls/aliases.
    for node in ast.walk(selection):
        if isinstance(node, (
            ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef,
            ast.With, ast.AsyncWith,
        )):
            return
        if isinstance(node, (ast.Name, ast.Attribute, ast.Subscript)) and isinstance(
            node.ctx, (ast.Store, ast.Del),
        ):
            base = node
            while isinstance(base, (ast.Attribute, ast.Subscript)):
                base = base.value
            if isinstance(base, ast.Name) and base.id == "instance":
                return
    selection._u16_preceding_coefficient_bound = True


def _coefficient_statement_covers(module: str, row: list, erased: dict, stop: ast.AST) -> bool:
    """Do not generalize the alternative to any other function, site or operand."""
    if not (
        module == row[0] == "sign_routing" and row[1] == "branch_coefficients"
        and row[3] in _COEFFICIENT_BOUND_PATHS and row[4] == "vertex"
        and row[5] == "range(instance.n)"
        and canonical(stop) == canonical(ast.parse("instance.n", mode="eval").body)
    ):
        return False
    selection = at_path(erased[row[1]], "body[7]")
    return bool(
        isinstance(selection, ast.If)
        and canonical(selection.test) == canonical(ast.parse("branch < 2", mode="eval").body)
        and getattr(selection, "_u16_preceding_coefficient_bound", False)
    )


def assert_source(name: str, source: bytes, tables: dict, reference: dict,
                  require_sites: bool = True) -> dict:
    # Discover the original occurrence universe before accepting any listed-site coverage.
    assert_inventory_complete(inventory_sources(reference, tables), tables)
    return _assert_source_after_inventory(name, source, tables, reference, require_sites)


def _assert_source_after_inventory(name: str, source: bytes, tables: dict, reference: dict,
                  require_sites: bool = True) -> dict:
    original = reference["files"][name]["source"]
    old_tree = ast.parse(original)
    text = source.decode()
    if name not in {"exactfrac/" + r[1] + ".py" for r in tables["U16_SCALAR_SITES"]
                    if r[10] in {"TAP_SCALAR", "OBSERVE_POST_STORE", "TAP_SUM_FINAL"}}:
        need(source == original.encode(), "immutable source changed " + name)
        return {"direct_sites": 0, "post_stores": 0}
    module = Path(name).stem
    original_functions = functions(old_tree)
    current_tree = ast.parse(text)
    current_functions = functions(current_tree)
    for row in tables["U16_FUNCTIONS"]:
        if row[0] == module and row[5] != "measured; recording-only taps permitted":
            need(row[1] in current_functions, "missing frozen function")
            need(ast.get_source_segment(text, current_functions[row[1]])
                 == ast.get_source_segment(original, original_functions[row[1]]),
                 "frozen function bytes changed " + name + ":" + row[1])
    # Mark immediate statement successors, independent of blank lines/formatting.
    for owner in ast.walk(current_tree):
        for _, sequence in ast.iter_fields(owner):
            if not isinstance(sequence, list):
                continue
            for previous, following in pairwise(sequence):
                if not isinstance(previous, ast.AugAssign) or not isinstance(following, ast.Expr):
                    continue
                call = following.value
                if not (isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
                        and call.func.id == "_observe_ints"):
                    continue
                wanted = canonical(ast.parse(ast.unparse(previous.target), mode="eval").body)
                previous._u16_post_observed = any(canonical(a) == wanted for a in call.args)
    for loop in ast.walk(current_tree):
        if not isinstance(loop, ast.For):
            continue
        first = loop.body[0] if loop.body else None
        call = first.value if isinstance(first, ast.Expr) else None
        if (isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
                and call.func.id == "_observe_ints"):
            loop._u16_entry_values = tuple(canonical(a) for a in call.args)
    _mark_coefficient_bound_statement(module, current_functions)
    allowed_functions = {r[1].split(".")[-1] for r in tables["U16_FUNCTIONS"]
                         if r[0] == module and r[5] == "measured; recording-only taps permitted"}
    eraser = Eraser(allowed_functions)
    erased = eraser.visit(current_tree)
    need(canonical(erased) == canonical(old_tree), "non-erasable mathematical edit " + name)
    erased_functions = functions(erased)
    direct = post = 0
    for row in tables["U16_SCALAR_SITES"]:
        if row[1] != module:
            continue
        old = at_path(original_functions[row[2]], row[7])
        need(digest(canonical(old).encode()) == row[8], "site AST identity " + row[0])
        new = at_path(erased_functions[row[2]], row[7])
        if require_sites and row[10] in {"TAP_SCALAR", "TAP_SUM_FINAL"}:
            need(getattr(new, "_u16_tapped", False), "unobserved scalar site " + row[0])
            direct += 1
        elif require_sites and row[10] == "OBSERVE_POST_STORE":
            need(isinstance(new, ast.AugAssign), "post-store shape")
            need(getattr(new, "_u16_post_observed", False),
                 "missing immediate post-store observation " + row[0])
            post += 1
        elif row[10].startswith("EXCLUDE") or row[10] in {"OUTSIDE", "DOMINATED_CONSTRUCTOR"}:
            need(not getattr(new, "_u16_tapped", False), "excluded expression tapped " + row[0])
    if require_sites and module == "solve":
        loop = next(n for n in ast.walk(erased_functions["solve"])
                    if isinstance(n, ast.For) and isinstance(n.target, ast.Name)
                    and n.target.id == "branch")
        need(all(getattr(n, "_u16_scope", None) == "branch" for n in loop.body),
             "branch scope does not cover every branch decision and comparison")
    if require_sites and module == "families":
        need(sum(event == "_record_prepared_sizes" for _, event, _, _ in eraser.observations) == 1,
             "one preparation event required")
    if require_sites:
        assert_iterator_roles(module, erased_functions, tables)
        assert_pair_roles(module, erased_functions, eraser)
    return {"direct_sites": direct, "post_stores": post}



def assert_iterator_roles(module: str, erased: dict, tables: dict) -> None:
    """Check the inventoried range bounds or freshly generated enumerate indices."""
    for row in tables["U16_ITERATOR_SITES"]:
        if row[0] != module or row[6] == "outside":
            continue
        iterator = at_path(erased[row[1]], row[3])
        call = iterator.iter
        need(isinstance(call, ast.Call) and isinstance(call.func, ast.Name),
             "unexpected registered iterator shape")
        if call.func.id == "range":
            stop = call.args[0] if len(call.args) == 1 else call.args[1]
            need(
                getattr(stop, "_u16_tapped", False)
                or _coefficient_statement_covers(module, row, erased, stop),
                "range bound not observed for D-ITER: " + row[0] + ":" + row[1],
            )
        else:
            need(call.func.id == "enumerate" and isinstance(iterator, ast.For),
                 "unexpected enumerate site")
            target = iterator.target.elts[0]
            index = ast.parse(ast.unparse(target), mode="eval").body
            need(canonical(index) in getattr(iterator, "_u16_entry_values", ()),
                 "generated enumerate index not observed at loop entry: " + row[1])


def assert_pair_roles(module: str, erased: dict, eraser: Eraser) -> None:
    """Bind raw-pair observations to original operands, not just function names."""
    pairs = {(fn, tuple(ast.unparse(a) for a in args)) for fn, event, args, _ in eraser.observations
             if event == "_observe_pair_values"}
    tuple_returns = {"rational": ("make_pair", "pair_add_one", "pair_reflect"),
                     "oracle": ("_source_terms",)}
    for name in tuple_returns.get(module, ()):
        returns = [n for n in ast.walk(erased[name]) if isinstance(n, ast.Return)]
        need(
            returns and all("_tap_pair" in getattr(n.value, "_u16_tap_kinds", ()) for n in returns),
            "returned raw pair not observed: " + name,
        )
    if module == "rational":
        need(("validate_pair", ("numerator", "checked_denominator")) in pairs
             or ("validate_pair", ("numerator", "denominator")) in pairs,
             "validated raw-pair operands not observed")
        last = erased["residual_numerator"].body[-1]
        need(isinstance(last, ast.Return)
             and "_tap_numerator" in getattr(last.value, "_u16_tap_kinds", ())
             and getattr(last.value, "_u16_denominator", None)
             == canonical(ast.Name(id="denominator", ctx=ast.Load())),
             "residual pair not bound to its submitted denominator")
    if module == "solve":
        need(("_endpoint", ("numerator", "denominator")) in pairs,
             "original endpoint-formula fields not observed")
        roots = [n.value for n in ast.walk(erased["_endpoint"])
                 if isinstance(n, ast.Assign) and ast.unparse(n.value) == "result.root"]
        need(("_endpoint", ("A", "B")) in pairs
             or any("_tap_pair" in getattr(n, "_u16_tap_kinds", ()) for n in roots),
             "returned branch-root operands not observed")
        need(("_evaluate", ("value.N", "value.D")) in pairs,
             "evaluated witness raw fields not observed")
    if module == "witness":
        call = erased["witness_value"].body[-1].value
        need(("witness_value", ("numerator", "denominator")) in pairs
             or (isinstance(call, ast.Call)
                 and "_tap_numerator" in getattr(call.args[0], "_u16_tap_kinds", ())
                 and getattr(call.args[0], "_u16_denominator", None)
                 == canonical(ast.Name(id="denominator", ctx=ast.Load()))),
             "witness constructor raw fields not observed")

def audit_legacy(root: Path = ROOT, require_sites: bool = True) -> dict:
    tables = load_tables(root)
    reference = load_reference(root)
    assert_inventory_complete(inventory_sources(reference, tables), tables)
    totals = {"direct_sites": 0, "post_stores": 0}
    recipes = {r["path"] for r in ADAPTER_RECIPES}
    need({(r["path"], r["function"]) for r in ADAPTER_RECIPES}
         == {(r[0], r[1]) for r in tables["U16_GUARD_ADAPTERS"]}, "adapter scope inventory")
    for name, record in reference["files"].items():
        source = (root / name).read_bytes()
        if name in recipes:
            need(source == expected_test(name, record["source"].encode(), tables),
                 "non-enumerated test change " + name)
        elif name.startswith("exactfrac/"):
            for key, value in _assert_source_after_inventory(
                name, source, tables, reference, require_sites,
            ).items():
                totals[key] += value
        else:
            need(source == record["source"].encode(), "frozen legacy file changed " + name)
    return {
        **totals,
        "legacy_files": len(reference["files"]),
        "guard_functions": len(ADAPTER_RECIPES),
    }
