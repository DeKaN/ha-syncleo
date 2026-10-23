"""Static (AST) checks of device profiles; no Home Assistant import needed."""

import ast
from pathlib import Path

_DEVICES = (
    Path(__file__).resolve().parent.parent / "custom_components" / "syncleo" / "devices"
)


def test_rusclimate_35_program_fields_match_spec():
    tree = ast.parse((_DEVICES / "humidifiers.py").read_text())
    pairs = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "ProgramDataField"
        ):
            kwargs = {kw.arg: ast.literal_eval(kw.value) for kw in node.keywords}
            pairs.add((kwargs["mode"], kwargs.get("offset", 0)))
    assert pairs == {
        (6, 0),
        (7, 0),
        (7, 1),
        (8, 0),
        (8, 1),
        (8, 2),
        (8, 3),
        (9, 0),
        (9, 1),
        (9, 2),
        (9, 3),
        (9, 4),
        (9, 5),
        (10, 0),
    }
