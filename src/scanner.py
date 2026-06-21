import os
from datetime import datetime

def scan_directory(path, extension=None):
    files = []
    entries = os.listdir(path)
    for entry in entries:
        full_path = os.path.join(path, entry)
        if os.path.isfile(full_path):
            if extension is None or full_path.endswith(extension):
                stat = os.stat(full_path)
                files.append({
                    "path": full_path,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime),
                })
        elif os.path.isdir(full_path):
            files += scan_directory(full_path, extension)
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