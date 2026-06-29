import os
from datetime import datetime

def scan_folder(path1, skip_extensions=None):
    if skip_extensions is None:
        skip_extensions = set()

    all_files = []

    def recurse(path2):
        try:
            vhod = os.listdir(path2)
        except (PermissionError, OSError):
            return

        for vh in vhod:
            all_path = os.path.join(path2, vh)

            if vh.startswith("."):
                continue

            if os.path.isdir(all_path):
                recurse(all_path)
            else:
                try:
                    _, ext = os.path.splitext(vh)
                    if ext.lower() in skip_extensions:
                        continue

                    size = os.path.getsize(all_path)
                    if size == 0:
                        continue

                    mtime_ts = os.path.getmtime(all_path)

                    all_files.append({
                        "path": all_path,
                        "size": size,
                        "modified": datetime.fromtimestamp(mtime_ts)
                    })
                except (PermissionError, OSError):
                    continue

    recurse(path1)
    return all_files

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