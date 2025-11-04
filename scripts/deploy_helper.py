"""deploy_helper.py — готовит проект к публикации"""
import subprocess
import shutil
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Подготовка к публикации")
    parser.add_argument(
        "--mode", choices=["sdist", "wheel", "both"], default="both")
    args = parser.parse_args()
    # Очистка старой сборки
    if Path("dist").exists():
        shutil.rmtree("dist")
    if args.mode in ["sdist", "both"]:
        subprocess.run(["python", "setup.py", "sdist"])
    if args.mode in ["wheel", "both"]:
        subprocess.run(["python", "setup.py", "bdist_wheel"])
    print("Публикация подготовлена")


if __name__ == "__main__":
    main()
