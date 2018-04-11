# -*- coding: utf-8 -*-


def get_filters(path):
    if path is None:
        return

    filters = []
    with open(path, encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            if "\n" in line:
                filters.append(line[:-1])
            else:
                filters.append(line)
    return filters


def main_0011():
    filters = get_filters("mingan.txt")
    print(filters)
    while 1:
        tmp = input("plz input: ")
        if tmp == "0":
            print("Exit")
            break
        else:
            if tmp in filters:
                print("Freedom")
            else: 
               print("Human Rights")


if __name__ == "__main__":
    main_0011()

