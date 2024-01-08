
# выявляем "п" группы, которые выложили наш пост спустя 3 дня и записываем в "p_sorted" в той же папке

# задать post_link
# записать путь к "п" группам в pathToFolder
# задать startFrom и goTo (нумерация с 1) - промежуток пулов, в которых выявляются "п" группы,
#   [от startFrom до goTo вкл], при том что файлы в папке в лексикографическом порядке

import vk_api
from data import my_token
import os
from pool import Pool

session = vk_api.VkApi(token=my_token)
vk = session.get_api()

post_link = ''
pathToFolder = "Pools/p"
startFrom = 1
goTo = 2

pathToPSorted = f"{pathToFolder[:pathToFolder.rfind('/')]}/p_sorted"
pathToCopy = f"{pathToFolder[:pathToFolder.rfind('/')]}/p_copy"
textFromPost = vk.wall.getById(posts=post_link[post_link.find('wall') + 4:])[0]["text"]
textFromPost = textFromPost[:textFromPost.find('\n')]
pools = []
counter = 1
for n, item in enumerate(os.listdir(pathToFolder)):
    if item[-4:] != '.txt' or item[:2] == '__':
        continue
    if startFrom <= counter <= goTo:
        pools.append(Pool(f"{pathToFolder}/{item}"))
    counter += 1

if not os.path.exists(pathToCopy):
    os.mkdir(pathToCopy)
for pool in pools:
    pool.write_back(pathToCopy + pool.path[len(pathToFolder):])

# print(f"|{textFromPost}|")
# for pool in pools:
#     print(f"\n{str(pool)}: {len(pool)}")
#     for group in pool:
#         print(str(group))

allGroups = 0
allPublished = 0
postsAtATime = 5
if not os.path.exists(pathToPSorted):
    os.mkdir(pathToPSorted)

for pool in pools:
    print(f"\n{str(pool)}: {len(pool)}")
    new_groups = []
    no = 1
    for group in pool:
        print(f"{no}) {group.screen_name} - ", end='')
        offset = 0
        try:
            vk.wall.get(owner_id=-group.id, count=1)
        except vk_api.exceptions.ApiError:
            print("blacklist")
            continue
        while True:
            posts = vk.wall.get(owner_id=-group.id, offset=offset, count=postsAtATime)["items"]
            if len(posts) == 0 or posts[-1]["id"] <= group.post_id:
                break
            offset += postsAtATime
        published = False
        vk_link = ''
        for post in posts:
            if textFromPost in post["text"]:
                published = True
                vk_link = f'{post["owner_id"]}_{post["id"]}'
                break
        if published:
            new_groups.append(group)
            print(f"опубликовали!  https://vk.com/{group.screen_name}?w=wall{vk_link}")
        else:
            print("no")
        no += 1
    print(f"Итого: из {len(pool)} групп {len(new_groups)} опубликовали пост")
    allGroups += len(pool)
    allPublished += len(new_groups)
    if len(new_groups):
        new_path = pathToPSorted + pool.path[pool.path.rfind('/'):]
        pool.write_back(new_path)
    os.remove(pool.path)

if len(os.listdir(pathToFolder)):
    os.rmdir(pathToFolder)

print(f"\n\nВ общем итоге: из {allGroups} групп {allPublished} опубликовали пост")
