"""doc_generator.py — генерирует документацию"""
import os
import subprocess
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Генерация документации")
    parser.add_argument("--docs-folder", default="docs", help="Папка для документации")
    args = parser.parse_args()
    docs_path = Path(args.docs_folder)
    if not docs_path.exists():
        docs_path.mkdir(parents=True)
    subprocess.run(["sphinx-quickstart", str(docs_path)])
    print(f"Документация создана в {docs_path}")

if __name__ == "__main__":
