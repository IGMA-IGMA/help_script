"""version_bump.py — повышает версию и обновляет changelog"""
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
        f.write(
            f"\n## {new_version} – {date.today()}\n- Авто-обновление версии\n")
    subprocess.run(["git", "add", str(file_path), str(changelog)])
    subprocess.run(["git", "commit", "-m", f"Bump version to {new_version}"])
    subprocess.run(["git", "tag", f"v{new_version}"])
    print(f"Версия обновлена: {version} → {new_version}")


if __name__ == "__main__":
    main()
