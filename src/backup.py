from scanner import scan_folder
from duplicates import get_file_hash


def check_backup(original, backup, extension=None):
    original_files = {}
    for f in scan_folder(original, extension):
        relative_path = f["path"][len(original):]
        original_files[relative_path] = get_file_hash(f["path"])

    backup_files = {}
    for f in scan_folder(backup, extension):
        relative_path = f["path"][len(backup):]
        backup_files[relative_path] = get_file_hash(f["path"])

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