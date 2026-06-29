import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from scanner import scan_folder, print_file_list
from duplicates import find_duplicates
from backup import check_backup

def main():
    args = sys.argv[1:]

    if len(args) == 0:
        print("Ошибка: Укажите путь к папке.")
        print("Использование:")
        print("  python main.py <папка> [<бэкап>] [--skip-ext .txt,.exe]")
        return

    skip_extensions = {".tmp", ".log", ".sys", ".md"}

    if "--skip-ext" in args:
        idx = args.index("--skip-ext")
        if idx + 1 < len(args):
            user_exts = args[idx + 1].split(",")
            skip_extensions = {f".{e.strip().lstrip('.')}".lower() for e in user_exts if e.strip()}
        del args[idx:idx + 2]

    original = args[0]
    backup = args[1] if len(args) > 1 else None

    print(f"\nСканирование: {original}")
    print(f"Пропускаются расширения: {', '.join(skip_extensions)}")
    print()

    files = scan_folder(original, skip_extensions)
    print_file_list(files)
    find_duplicates(files)

    if backup:
        check_backup(original, backup, skip_extensions)

if __name__ == "__main__":
    main()