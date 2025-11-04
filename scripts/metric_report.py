"""metric_report.py — собирает метрики проекта"""
import os
from pathlib import Path


def count_py_files(root: Path):
    return sum(1 for _, _, filenames in os.walk(root) for f in filenames if f.endswith(".py"))


def count_lines(root: Path):
    total = 0
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.endswith(".py"):
                with open(Path(dirpath) / f, "r", encoding="utf-8") as file:
                    total += len(file.readlines())
    return total


def main():
    root = Path(".").resolve()
    print(f"Сбор метрик для {root}")
    num_files = count_py_files(root)
    print(f".py файлов: {num_files}")
    num_lines = count_lines(root)
    print(f"Строк кода (.py файлов): {num_lines}")


if __name__ == "__main__":
    main()
