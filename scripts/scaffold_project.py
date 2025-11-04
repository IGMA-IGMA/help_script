"""scaffold_project.py — создаёт каркас нового проекта"""
import os
from pathlib import Path
import subprocess
import argparse


def create_structure(project_name: str, base_dir: Path):
    structure = [
        base_dir / project_name / "src",
        base_dir / project_name / "tests",
        base_dir / project_name / "docs"
    ]
    for path in structure:
        path.mkdir(parents=True, exist_ok=True)
    # README.md
    with open(base_dir / project_name / "README.md", "w", encoding="utf-8") as f:
        f.write(f"# {project_name}\n\nОписание проекта.")
    # requirements.txt
    with open(base_dir / project_name / "requirements.txt", "w", encoding="utf-8") as f:
        f.write("# Добавьте зависимости\n")
    # .gitignore
    with open(base_dir / project_name / ".gitignore", "w", encoding="utf-8") as f:
        f.write("__pycache__/\n*.pyc\n.env\n")
    # Инициализация git
    subprocess.run(["git", "init", str(base_dir / project_name)])
    print(f"Создан проект {project_name} в {base_dir / project_name}")


def main():
    parser = argparse.ArgumentParser(
        description="Создать каркас нового проекта")
    parser.add_argument("--project-name", required=True, help="Имя проекта")
    parser.add_argument("--base-dir", default=".", help="Базовая папка")
    args = parser.parse_args()
    base_dir = Path(args.base_dir).resolve()
    create_structure(args.project_name, base_dir)


if __name__ == "__main__":
    main()
