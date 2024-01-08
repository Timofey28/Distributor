from data import V, my_token
import requests
import os
import time
import shutil
from distutils.dir_util import copy_tree

main_token = my_token
time_interval = 3600 * 24 * 30  # в секундах

if os.path.exists("Pools/raw_copy"):
    shutil.rmtree("Pools/raw_copy")
os.mkdir("Pools/raw_copy")
copy_tree("Pools/raw", "Pools/raw_copy")

startFrom = 1  # с какого файла начать (нумерация с 1)

for n, item in enumerate(os.listdir("Pools/raw")):
    if n < startFrom - 1:
        continue
    if item[-4:] != '.txt' or item[:2] == '__':
        continue
    with open(f"Pools/raw/{item}") as file:
        groups = file.readlines()
    groups = list(filter(lambda x: x != '\n', groups))
    ids = list(map(int, groups))
    current_time = round(time.time())
    new_groups = []

    print(f"\n\t{item[:-4].replace('_', ' ')} ({len(groups)}):\n")
    for i in range(0, len(ids)):
        print(f"\t{i + 1}) {ids[i]} club{ids[i]} ", end='')

        try:
            info = requests.get(f"https://api.vk.com/method/groups.getById?group_id={ids[i]}&access_token={main_token}&v={V}").json()["response"][0]
            if info["is_closed"] == 1:
                print("группа закрыта")
                continue
        except:
            print("с этим аккаунтом все")
            exit(-1)

        offset = 2
        src = requests.get(f"https://api.vk.com/method/wall.get?owner_id=-{ids[i]}&count=2&access_token={main_token}&v={V}").json()
        if "response" not in src or len(src["response"]["items"]) == 0:
            print("в группе нет постов")
            continue
        else:
            src = src["response"]["items"]
        if ("views" in src[0] or src[0]["likes"]["count"] > 0 or src[0]["comments"]["count"] > 0 or ("reposts" in src[0] and src[0]["reposts"]["count"] > 0)) and src[0]["date"] > current_time - 3600 * 24 * 30:
            print(f"активность имеется")
            new_groups.append(groups[i])
            continue
        while src[-1]["date"] > current_time - time_interval and "views" not in src[-1] and src[-1]["likes"]["count"] == 0 and src[-1]["comments"]["count"] == 0 and "reposts" in src[-1] and src[-1]["reposts"]["count"] == 0:
            sr = requests.get(f"https://api.vk.com/method/wall.get?owner_id=-{ids[i]}&count=1&offset={offset}&access_token={main_token}&v={V}").json()["response"]["items"]
            if not sr:
                break
            src.extend(sr)
            offset += 1
        if ("views" in src[-1] or src[-1]["likes"]["count"] > 0 or src[-1]["comments"]["count"] > 0 or ("reposts" in src[-1] and src[-1]["reposts"]["count"] > 0)) and src[-1]["date"] > current_time - time_interval:
            print(f"активность имеется")
            new_groups.append(groups[i])
        else:
            print(f"нет")

    with open(f"Pools/raw/{item}", "w") as file:
        file.writelines(new_groups)
