import sys
import os
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


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        print(f"Сканирование: {path}\n")
        files = scan_directory(path)
        print_file_list(files)
    else:
        print("Ошибка: Укажите путь")


if __name__ == "__main__":
    main()
