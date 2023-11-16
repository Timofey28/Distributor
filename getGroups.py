import vk_api
from data import my_token
import os


session = vk_api.VkApi(token=my_token)
vk = session.get_api()

reqs = [
    '',
    '',
    '',
]


def getGroupsJson(allGroups):
    newGroups = []
    counter = 1
    for req in reqs:
        current_groups = vk.groups.search(q=req.lower(), type='group,page', count=1000)  # city_id=1 если нужно по Москве
        pool_name = req.lower()
        pool_name = pool_name.replace(' ', '_')
        pool_name = pool_name[0].upper() + pool_name[1:]
        summa = 0
        for group in current_groups["items"]:
            if group["id"] not in newGroups and group["id"] not in allGroups:
                newGroups.append(group["id"])
                summa += 1
                with open(f"Pools/raw/{pool_name}.txt", "a", encoding="utf-8") as file:
                    file.write(str(group["id"]) + '\n')
        print(f'\t{counter}) {current_groups["count"]}\t\t({summa} записано)')
        counter += 1
    print(f"\n\tИтого: {len(newGroups)} групп")


if __name__ == '__main__':
    if not os.path.exists("Pools"):
        os.mkdir("Pools")
    if not os.path.exists("Pools/raw"):
        os.mkdir("Pools/raw")
    allGroups = []
    for n, item in enumerate(os.listdir("Pools")):
        if item[-4:] != '.txt' or item[:2] == '__':
            continue
        if item[:-4].replace('_', ' ').lower() in reqs:
            reqs.remove(item[:-4].replace('_', ' ').lower())
        with open(f"Pools/{item}") as file:
            groups = file.readlines()
        groups = list(filter(lambda x: x != '\n', groups))
        groups = list(map(lambda x: int(x[:x.find(' ')]), groups))
        allGroups.extend(groups)
    getGroupsJson(allGroups)
