import hashlib

def get_file_hash(path):

    hasher = hashlib.md5()
    with open(path, "rb") as f:
        chunk = f.read(4096)
        while chunk:
            hasher.update(chunk)
            chunk = f.read(4096)
    return hasher.hexdigest()

def find_duplicates(files):
    hashes = {}
    for f in files:
        file_hash = get_file_hash(f["path"])
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