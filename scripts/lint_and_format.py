"""lint_and_format.py — запускает линтеры и форматтеры"""
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser(description="Lint and format project")
    parser.add_argument("--fix", action="store_true", help="Авто-исправление")
    args = parser.parse_args()
    cmd = ["flake8", "."]
    subprocess.run(cmd)
    if args.fix:
        subprocess.run(["isort", "."])
        subprocess.run(["black", "."])
        print("Форматирование и сортировка импортов выполнены")
    print("Lint/format проверка завершена")


if __name__ == "__main__":
    main()
