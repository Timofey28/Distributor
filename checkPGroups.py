
# выявляем "п" группы, которые выложили наш пост спустя 3 дня и записываем в другую папку "p_sorted" в той же
# директории

# записать кусок текста из поста в textInPost
# записать путь к "п" группам в pathToFolder
# задать startFrom и goTo (номера с 1) - промежуток пулов, в которых выявляются "п" группы,
#   [от startFrom до goTo вкл], притом что файлы в папке в лексикографическом порядке

import vk_api
from data import my_token
import os
import copy
from distutils.dir_util import copy_tree
import shutil


session = vk_api.VkApi(token=my_token)
vk = session.get_api()

textInPost = 'Не важно, где вы находитесь и какой у вас участок.'
pathToFolder = "Pools/p"
pathToPSorted = f"{pathToFolder[:pathToFolder.rfind('/')]}/p_sorted"
paths = []  # пути пулов
pools = []  # в элементе: [groups, group_ids, screen_names, post_ids]
# groups для того, чтобы потом записать обратно "отредактированные" группы
# обращаемся через group_ids, screen_names чисто для вывода в консоль
for n, item in enumerate(os.listdir(pathToFolder)):
    paths.append(pathToFolder + '/' + item)
    with open(f"{pathToFolder}/{item}") as file:
        lines = file.readlines()
    groups = copy.copy(lines)
    group_ids = list(map(lambda x: int(x[:x.find(' ')]), lines))
    post_ids = list(map(lambda x: int(x[x.rfind(' ') + 1:]), lines))
    lines = list(map(lambda x: x[x.find(' ') + 1:], lines))
    screen_names = list(map(lambda x: x[:x.find(' ')], lines))
    pools.append([groups, group_ids, screen_names, post_ids])

path_copy = pathToFolder[:pathToFolder.rfind('/') + 1] + "p_copy"
if os.path.exists(path_copy):
    shutil.rmtree(path_copy)
os.mkdir(path_copy)
copy_tree(pathToFolder, path_copy)

# for pool in pools:
#     print("\n\t")
#     print(len(pool[0]) == len(pool[1]) == len(pool[2]) == len(pool[3]))
#     print("groups:", pool[0])
#     print("group_ids:", pool[1])
#     print("screen_names:", pool[2])
#     print("post_ids:", pool[3])

startFrom = 1
goTo = 3

allGroups = 0
allPublished = 0
if not os.path.exists(pathToPSorted):
    os.mkdir(pathToPSorted)
for i in range(max(0, startFrom - 1), min(len(pools), goTo)):
    print(f"\n\t{i + 1}. {paths[i][len(pathToFolder) + 1:-7].replace('_', ' ')}  {len(pools[i][0])}\n")
    new_pool = []
    for j in range(len(pools[i][0])):
        print(f"\t{j + 1}) {pools[i][2][j]} - ", end='')
        offset = 0
        try:
            vk.wall.get(owner_id=-int(pools[i][1][j]), count=1)
        except vk_api.exceptions.ApiError:
            print("blacklist")
            continue
        while True:
            posts = vk.wall.get(owner_id=-int(pools[i][1][j]), offset=offset, count=5)["items"]
            if len(posts) == 0 or posts[-1]["id"] <= pools[i][3][j]:
                break
            offset += 5
        published = False
        vk_link = ''
        for post in posts:
            if textInPost in post["text"]:
                published = True
                vk_link = f'{post["owner_id"]}_{post["id"]}'
                break
        if published:
            new_pool.append(pools[i][0][j])
            print(f"опубликовали!  https://vk.com/{pools[i][2][j]}?w=wall{vk_link}")
        else:
            print("no")
    print(f"\n\tИтого: из {len(pools[i][0])} групп {len(new_pool)} опубликовали пост")
    allGroups += len(pools[i][0])
    allPublished += len(new_pool)
    if len(new_pool):
        new_path = pathToPSorted + paths[i][paths[i].rfind('/'):]
        with open(new_path, "w", encoding="utf-8") as file:
            for np in new_pool:
                file.write(str(np))
    os.remove(paths[i])

print(f"\n\n\tВ общем итоге: из {allGroups} групп {allPublished} опубликовали пост")
