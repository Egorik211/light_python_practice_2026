import sys
import os
import hashlib
from datetime import datetime

def scan_directory(path):
    files = []
    entries = os.listdir(path)
    for entry in entries:
        full_path = os.path.join(path, entry)
        if os.path.isfile(full_path):
            stat = os.stat(full_path)
            files.append({
                "path": full_path,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime),
            })
        elif os.path.isdir(full_path):
            files += scan_directory(full_path)
    return files

def format_size(size_bytes):
    for unit in ("Б", "КБ", "МБ", "ГБ"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} ТБ"

def print_file_list(files):
    for f in files:
        size = format_size(f["size"])
        date = f["modified"].strftime("%Y-%m-%d %H:%M")
        print(f"{f['path']}  |  {size}  |  {date}")
    print(f"\nИтого: {len(files)} файл(ов)")

def find_duplicates(files):
    hashes = {}
    for f in files:
        content = open(f["path"], "rb").read()
        file_hash = hashlib.md5(content).hexdigest()
        if file_hash not in hashes:
            hashes[file_hash] = []
        hashes[file_hash].append(f["path"])

    print("\n Дубликаты \n")
    found = False
    for file_hash, paths in hashes.items():
        if len(paths) >= 2:
            found = True
            print(f"Хэш: {file_hash}")
            for path in paths:
                print(f"  {path}")
            print()
    if not found:
        print("Дубликаты не найдены.")

def check_backup(original, backup):
    original_files = {}
    for f in scan_directory(original):
        relative_path = f["path"][len(original):]
        original_files[relative_path] = f["size"]

    backup_files = {}
    for f in scan_directory(backup):
        relative_path = f["path"][len(backup):]
        backup_files[relative_path] = f["size"]

    print("\n Сравнение с бэкапом \n")
    for name in original_files:
        if name not in backup_files:
            print(f"Отсутствует в бэкапе:  {name}")
        elif original_files[name] != backup_files[name]:
            print(f"Изменён:               {name}")
    for name in backup_files:
        if name not in original_files:
            print(f"Лишний в бэкапе:       {name}")
    print("\nСравнение завершено.")

def main():
    if len(sys.argv) == 3:
        original, backup = sys.argv[1], sys.argv[2]
        print(f"Сканирование: {original}\n")
        files = scan_directory(original)
        print_file_list(files)
        find_duplicates(files)
        check_backup(original, backup)
    elif len(sys.argv) == 2:
        path = sys.argv[1]
        print(f"Сканирование: {path}\n")
        files = scan_directory(path)
        print_file_list(files)
        find_duplicates(files)
    else:
        print("Ошибка: Укажите путь")

if __name__ == "__main__":
    main()
