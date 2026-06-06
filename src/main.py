import sys

def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        print(path)
    else:
        print("Ошибка: Укажите путь")

if __name__ == "__main__":
    main()


