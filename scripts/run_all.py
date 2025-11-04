"""run_all.py — Запускает все скрипты по очереди"""

import subprocess
import sys
from pathlib import Path


def run_script(script_path):
    cmd = [sys.executable, str(script_path)]
    print(f"→ Запуск: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(
            f"!! Ошибка: скрипт {script_path.name} завершился с кодом {result.returncode}")
        sys.exit(result.returncode)
    print(f"✔ Скрипт {script_path.name} успешно завершён\n")


def main():
    root = Path.cwd()
    scripts_folder = root / ""
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
    main()
