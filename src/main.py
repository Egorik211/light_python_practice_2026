import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from scanner import scan_directory, print_file_list
from duplicates import find_duplicates
from backup import check_backup

def main():
    args = sys.argv[1:]

    if len(args) == 0:
        print("Ошибка: Укажите путь")
        print("Использование:")
        print("  python main.py <папка>")
        print("  python main.py <папка> <бэкап>")
        return

    original = args[0]
    backup = args[1] if len(args) > 1 else None

    extension = input("Введите расширение для фильтра или нажмите Enter чтобы пропустить: ")
    extension = extension.strip() or None

    print(f"\nСканирование: {original}\n")
    files = scan_directory(original, extension)
    print_file_list(files)
    find_duplicates(files)

    if backup:
        check_backup(original, backup, extension)

if __name__ == "__main__":
    main()