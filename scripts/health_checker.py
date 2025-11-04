"""health_checker.py — анализ проекта: зависимости, тесты, форматирование"""
import os
import ast
from pathlib import Path


def find_py_files(root: Path):
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.endswith(".py"):
                yield Path(dirpath) / f


def list_imports(py_path: Path):
    with open(py_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=str(py_path))
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return imports


def main():
    root = Path(".").resolve()
    print(f"Начало проверки проекта в {root}")
    py_files = list(find_py_files(root))
    print(f"Найдено {len(py_files)} .py файлов")
    all_imports = []
    for p in py_files:
        all_imports.extend(list_imports(p))
    unique_imports = set(all_imports)
    print(f"Уникальных импортов: {len(unique_imports)}")
    # TODO: добавить проверку неиспользуемых импортов, тестов, форматирования


main()
