import os


path_to_folder = "Pools"

if os.path.exists(f"{path_to_folder}/__количество__.txt"):
    os.remove(f"{path_to_folder}/__количество__.txt")

total = 0
files_amount = 0
for n, item in enumerate(os.listdir(path_to_folder)):
    if item[-4:] != '.txt' or item[:2] == '__':
        continue
    files_amount += 1
    title = item[:-4].replace('_', ' ')
    with open(f"{path_to_folder}/{item}") as file:
        lines = len(file.readlines())
    total += lines
    with open(f"{path_to_folder}/__количество__.txt", "a", encoding="utf-8") as file:
        file.write(f'"{title}": {lines}\n')

if files_amount > 0:
    with open(f"{path_to_folder}/__количество__.txt", "a", encoding="utf-8") as file:
        file.write(f'\nИтого: {total}\n')
