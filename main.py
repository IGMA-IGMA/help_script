# main.py

import os
from pathlib import Path
import textwrap

# Шаблоны файлов
README_TEMPLATE = """\
# Help Script Tools

Набор скриптов для ускорения разработки на Python: проект-стартер, проверки, документация, деплой и др.

## Структура

- `config.yaml` — глобальные настройки (пути, шаблоны, опции).
- `requirements.txt` — зависимости (если есть).
- `scripts/` — папка со скриптами:
  - `scaffold_project.py` — создаёт каркас нового проекта.
  - `health_checker.py` — анализирует проект.
  - `metric_report.py` — собирает метрики проекта.
  - `version_bump.py` — повышает версию проекта.
  - `git_cleanup.py` — очищает локальные ветки и т.д.
  - `doc_generator.py` — генерирует документацию.
  - `deploy_helper.py` — подготавливает проект к публикации.
  - `lint_and_format.py` — запускает линтеры и форматтеры.
  - `run_all.py` — запускает все скрипты по очереди.
  - `custom_script.py` — ваш дополнительный скрипт.
  
## Как начать

1. В корне проекта запустите `python main.py`
2. После выполнения настройте `config.yaml`, добавьте реальный код в скрипты.
3. Затем запускайте нужные скрипты.

## Лицензия

(добавьте вашу лицензию)
"""

CONFIG_TEMPLATE = """\
# Настройки для Help Script Tools
project_root: .
scripts_folder: scripts
templates_folder: templates
"""

REQUIREMENTS_TEMPLATE = """\
# Добавьте сюда зависимости, например:
# black
# isort
# flake8
"""

SCAFFOLD_PROJECT_CODE = """\
\"\"\"scaffold_project.py — создаёт каркас нового проекта\"\"\"
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
        f.write(f"# {project_name}\\n\\nОписание проекта.")
    # requirements.txt
    with open(base_dir / project_name / "requirements.txt", "w", encoding="utf-8") as f:
        f.write("# Добавьте зависимости\\n")
    # .gitignore
    with open(base_dir / project_name / ".gitignore", "w", encoding="utf-8") as f:
        f.write("__pycache__/\\n*.pyc\\n.env\\n")
    # Инициализация git
    subprocess.run(["git", "init", str(base_dir / project_name)])
    print(f\"Создан проект {project_name} в {base_dir / project_name}\")

def main():
    parser = argparse.ArgumentParser(description="Создать каркас нового проекта")
    parser.add_argument("--project-name", required=True, help="Имя проекта")
    parser.add_argument("--base-dir", default=".", help="Базовая папка")
    args = parser.parse_args()
    base_dir = Path(args.base_dir).resolve()
    create_structure(args.project_name, base_dir)

if __name__ == "__main__":
"""

HEALTH_CHECKER_CODE = """\
\"\"\"health_checker.py — анализ проекта: зависимости, тесты, форматирование\"\"\"
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

if __name__ == "__main__":
"""

METRIC_REPORT_CODE = """\
\"\"\"metric_report.py — собирает метрики проекта\"\"\"
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
"""

VERSION_BUMP_CODE = """\
\"\"\"version_bump.py — повышает версию и обновляет changelog\"\"\"
import toml
from pathlib import Path
from datetime import date
import argparse
import subprocess
import sys

def bump_version(version_str: str) -> str:
    major, minor, patch = map(int, version_str.split("."))
    patch += 1
    return f"{major}.{minor}.{patch}"

def main():
    parser = argparse.ArgumentParser(description="Обновить версию проекта")
    parser.add_argument("--file", default="pyproject.toml", help="Файл версии")
    args = parser.parse_args()
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Файл не найден: {file_path}")
        sys.exit(1)
    data = toml.load(file_path)
    version = data["tool"]["poetry"]["version"]
    new_version = bump_version(version)
    data["tool"]["poetry"]["version"] = new_version
    with open(file_path, "w", encoding="utf-8") as f:
        toml.dump(data, f)
    changelog = Path("CHANGELOG.md")
    with open(changelog, "a", encoding="utf-8") as f:
        f.write(f"\\n## {new_version} – {date.today()}\\n- Авто-обновление версии\\n")
    subprocess.run(["git", "add", str(file_path), str(changelog)])
    subprocess.run(["git", "commit", "-m", f\"Bump version to {new_version}\"])
    subprocess.run(["git", "tag", f\"v{new_version}\"])
    print(f"Версия обновлена: {version} → {new_version}")

if __name__ == "__main__":
"""

GIT_CLEANUP_CODE = """\
\"\"\"git_cleanup.py — очищает локальные ветки и stale-теги\"\"\"
import subprocess
import sys

def main():
    print("Fetching and pruning local git repository")
    subprocess.run(["git", "fetch", "--prune"])
    result = subprocess.run(["git", "branch", "-vv"], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    for l in lines:
        if "[gone]" in l:
            branch = l.split()[0]
            print(f"Предлагается удалить ветку: {branch}")
    # TODO: автоматическое удаление веток после подтверждения
    print("Готово")

if __name__ == "__main__":
"""

DOC_GENERATOR_CODE = """\
\"\"\"doc_generator.py — генерирует документацию\"\"\"
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
"""

DEPLOY_HELPER_CODE = """\
\"\"\"deploy_helper.py — готовит проект к публикации\"\"\"
import subprocess
import shutil
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Подготовка к публикации")
    parser.add_argument("--mode", choices=["sdist", "wheel", "both"], default="both")
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
"""

LINT_AND_FORMAT_CODE = """\
\"\"\"lint_and_format.py — запускает линтеры и форматтеры\"\"\"
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
"""

RUN_ALL_CODE = """\
\"\"\"run_all.py — Запускает все скрипты по очереди\"\"\"

import subprocess
import sys
from pathlib import Path

def run_script(script_path):
    cmd = [sys.executable, str(script_path)]
    print(f"→ Запуск: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"!! Ошибка: скрипт {script_path.name} завершился с кодом {result.returncode}")
        sys.exit(result.returncode)
    print(f"✔ Скрипт {script_path.name} успешно завершён\\n")

def main():
    root = Path.cwd()
    scripts_folder = root / "scripts"
    sequence = [
        "scaffold_project.py",
        "health_checker.py",
        "metric_report.py",
        "version_bump.py",
        "git_cleanup.py",
        "doc_generator.py",
        "deploy_helper.py",
        "lint_and_format.py",
    ]
    for name in sequence:
        path = scripts_folder / name
        if not path.exists():
            print(f"!! Не найден скрипт: {path}")
            sys.exit(1)
        run_script(path)
    print("=== Все скрипты успешно выполнены ===")

if __name__ == "__main__":
"""

CUSTOM_SCRIPT_CODE = """\
\"\"\"custom_script.py — ваш дополнительный скрипт\"\"\"

def main():
    print("custom_script.py – запуск")
    # TODO: добавьте логику вашего скрипта

if __name__ == "__main__":
    main()
"""

def create_structure(base_path: Path):
    paths = {
        "scripts": base_path / "scripts",
        "templates": base_path / "templates",
        "utils": base_path / "utils",
    }
    for p in paths.values():
        p.mkdir(parents=True, exist_ok=True)
        print(f"Создана папка: {p}")

    files = {
        "README.md": README_TEMPLATE,
        "config.yaml": CONFIG_TEMPLATE,
        "requirements.txt": REQUIREMENTS_TEMPLATE,
    }
    for fname, content in files.items():
        fpath = base_path / fname
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(textwrap.dedent(content))
        print(f"Создан файл: {fpath}")

    script_codes = {
        "scaffold_project.py": SCAFFOLD_PROJECT_CODE,
        "health_checker.py": HEALTH_CHECKER_CODE,
        "metric_report.py": METRIC_REPORT_CODE,
        "version_bump.py": VERSION_BUMP_CODE,
        "git_cleanup.py": GIT_CLEANUP_CODE,
        "doc_generator.py": DOC_GENERATOR_CODE,
        "deploy_helper.py": DEPLOY_HELPER_CODE,
        "lint_and_format.py": LINT_AND_FORMAT_CODE,
        "run_all.py": RUN_ALL_CODE,
        "custom_script.py": CUSTOM_SCRIPT_CODE,
    }

    for fname, code in script_codes.items():
        fpath = paths["scripts"] / fname
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(textwrap.dedent(code))
        print(f"Создан скрипт с кодом: {fpath}")

    print("\nСтруктура проекта создана и файлы заполнены кодом-шаблонами.")

def main():
    base_path = Path.cwd()
    print(f"Создание структуры проекта в папке: {base_path}")
    create_structure(base_path)

if __name__ == "__main__":
    main()
