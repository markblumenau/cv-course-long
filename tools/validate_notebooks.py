"""Проверяет формат ноутбуков и идентификаторы ячеек."""

import json
import sys
from pathlib import Path

import nbformat


def validate(path):
    notebook = json.loads(path.read_text(encoding="utf-8"))
    ids = [cell.get("id") for cell in notebook["cells"]]
    if any(not cell_id for cell_id in ids) or len(ids) != len(set(ids)):
        raise ValueError("Нужны уникальные непустые идентификаторы ячеек")
    nbformat.validate(notebook)


if __name__ == "__main__":
    failed = False
    for filename in sys.argv[1:]:
        try:
            validate(Path(filename))
        except (OSError, ValueError, nbformat.ValidationError) as error:
            failed = True
            print(f"{filename}: {error}", file=sys.stderr)
    sys.exit(int(failed))
