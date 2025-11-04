"""git_cleanup.py — очищает локальные ветки и stale-теги"""
import subprocess
import sys


def main():
    print("Fetching and pruning local git repository")
    subprocess.run(["git", "fetch", "--prune"])
    result = subprocess.run(["git", "branch", "-vv"],
                            capture_output=True, text=True)
    lines = result.stdout.splitlines()
    for l in lines:
        if "[gone]" in l:
            branch = l.split()[0]
            print(f"Предлагается удалить ветку: {branch}")
    # TODO: автоматическое удаление веток после подтверждения
    print("Готово")


if __name__ == "__main__":
    main()
