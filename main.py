import vk_api
import requests
from data import my_token, V, my_id, t1, t2, t3
import os
import time
from datetime import datetime
from pick import pick
import shutil

helper_token = t3
tokens = [t1, t2]
token_names = ['Имя аккаунта 1', 'Имя аккаунта 2']
limit_posts = [100, 100]

post_link = ''
current_post_send_counter: list
active_tokens = []
active_token_names = []
active_token_limits = []
posts_published: list
tok_nums = []
banned = []


def main():
    global post_link, current_post_send_counter, active_tokens, posts_published, tok_nums, banned
    checkAccounts()

    last_opened = datetime.fromtimestamp(os.path.getmtime("Pools/tech_part/accounts.txt"))
    now = datetime.now()
    day_start = datetime(now.year, now.month, now.day, 0, 0, 0)
    with open("Pools/tech_part/accounts.txt") as file:
        posts_published = list(filter(lambda x: x != '\n', file.readlines()))
    posts_published = list(map(int, posts_published))
    for i in range(len(posts_published)):
        if posts_published[i] == -1 and i not in banned:
            posts_published[i] = 0
        if posts_published[i] != -1:
            if i in banned:
                posts_published[i] = -1
                continue
            active_tokens.append(tokens[i])
            active_token_names.append(token_names[i])
            active_token_limits.append(limit_posts[i])
            tok_nums.append(i)
            if last_opened < day_start:
                posts_published[i] = 0

    with open("Pools/tech_part/current_post_send_counter.txt") as file:
        current_post_send_counter = list(filter(lambda x: x != '\n', file.readlines()))
    current_post_send_counter = list(map(int, current_post_send_counter))
    index = 0
    for n, item in enumerate(os.listdir("Pools")):
        if item[-4:] != '.txt' or item[:2] == '__':
            continue
        with open(f"Pools/{item}") as file:
            groups = list(filter(lambda x: x != '\n', file.readlines()))
        if current_post_send_counter[index] > len(groups):
            current_post_send_counter[index] = len(groups)
        index += 1

    if cantPublishAnymore():
        os.system("cls")
        print("\n\tНа сегодня лимит постов исчерпан, придется подождать до завтра")
        showPools(True)
        exit(0)

    index = 0
    while True:
        groupsAmount = 0
        for n, item in enumerate(os.listdir("Pools")):
            if item[-4:] != '.txt' or item[:2] == '__':
                continue
            with open(f"Pools/{item}") as file:
                pool = list(filter(lambda x: x != '\n', file.readlines()))
            groupsAmount += len(pool)

        title = f"   Всего активных групп: {groupsAmount}"
        options = ["Запустить рассылку", "Пулы", "Текущее количество публикаций с аккаунтов", "Поменять/посмотреть пост", "Собрать статистику", "Удалить группу", "Выход"]
        option, index = pick(options, title, indicator='=>', default_index=index if index else 0)
        if option == "Запустить рассылку":
            runSpam()
        elif option == "Пулы":
            os.system("cls")
            showPools()
        elif option == "Текущее количество публикаций с аккаунтов":
            os.system("cls")
            print("\n\tАккаунт\t\tТекущее количество публикаций\tЛимит\n")
            for i in range(len(active_tokens)):
                if tok_nums[i] in banned:
                    continue
                status = posts_published[tok_nums[i]]
                curr_limit = 3 if status == 100 else 2 if status >= 10 else 1
                print(f"\t{i + 1}) {active_token_names[i]}{' ' * (13 - len(active_token_names[i]))}{status}{' ' * (32 - curr_limit)}{active_token_limits[i]}")
            input()
        elif option == "Поменять/посмотреть пост":
            changePostLink()
        elif option == "Собрать статистику":
            getStatistics()
        elif option == "Удалить группу":
            deleteGroup()
        else:
            with open("Pools/tech_part/accounts.txt", "w") as file:
                file.writelines(list(map(lambda x: str(x) + '\n', posts_published)))
            with open("Pools/tech_part/current_post_send_counter.txt", "w") as file:
                file.writelines(list(map(lambda x: str(x) + '\n', current_post_send_counter)))
            os.system("cls")
            exit(0)


def runSpam():
    global post_link, current_post_send_counter, active_tokens, posts_published, tok_nums

    os.system("cls")
    if post_link == "":
        changePostLink()
    if post_link == "":
        return

    owner_id_and_post_id = post_link[post_link.find('wall') + 4:]
    url = f"https://api.vk.com/method/wall.getById?posts={owner_id_and_post_id}&access_token={my_token}&v={V}"
    src = requests.get(url).json()["response"][0]

    message = src["text"]
    attachments = ""
    for attach in src["attachments"]:
        if attach["type"] == "link" and "://" in attachments:
            continue
        if attachments != "":
            attachments += ','
        if attach["type"] == "link":
            attachments += attach["link"]["url"]
        else:
            attachments += attach["type"] + str(attach[attach["type"]]["owner_id"]) + '_' + str(attach[attach["type"]]["id"])

    os.system("cls")
    publications = 0  # сколько постов еще можно опубликовать
    for i in range(len(posts_published)):
        if posts_published[i] != -1:
            publications += limit_posts[i] - posts_published[i]

    title = "   В какие группы кидать пост? (перемещение - вверх/вниз, выбрать - пробел)\n"
    title += f"   Еще можно опубликовать {pickUpRightWordEnding(publications, 'пост', 'поста', 'постов')}"
    options = []

    nSpaces = 0
    for n, item in enumerate(os.listdir("Pools")):
        if item[-4:] != '.txt' or item[:2] == '__':
            continue
        nSpaces = max(nSpaces, len(item))
    nSpaces += 4
    index = -1
    for n, item in enumerate(os.listdir("Pools")):
        if item[-4:] != '.txt' or item[:2] == '__':
            continue
        index += 1
        with open(f"Pools/{item}") as file:
            temp = list(filter(lambda x: x != '\n', file.readlines()))
        option = f'{item[:-4].replace("_", " ")} {"-" * (nSpaces - len(item) - 2)} '
        if current_post_send_counter[index] >= len(temp):
            option += "отправлен во все группы"
        else:
            option += f"{current_post_send_counter[index]} из {len(temp)}"
        options.append(option)
    options.append("*** Вернуться назад ***")
    selected = pick(options, title, indicator='=>', multiselect=True, min_selection_count=1)
    indexes = list(map(lambda x: int(x[1]), selected))
    if len(options) - 1 in indexes:
        return
    paths = list(map(lambda x: x[0][:x[0].find('--') - 1].replace(' ', '_') + ".txt", selected))

    if os.path.exists("Pools/backup"):
        shutil.rmtree("Pools/backup")
    os.mkdir("Pools/backup")
    for n, item in enumerate(os.listdir("Pools")):
        if item[-4:] != '.txt' or item[:2] == '__':
            continue
        shutil.copyfile(f"Pools/{item}", f"Pools/backup/{item}")
        # удаляем из строк post_id в конце перед рассылкой нового поста
        if not any(current_post_send_counter):  # если все элементы c_p_s_c равны 0 (показатель замены ссылки)
            with open(f"Pools/{item}") as file:
                groups = list(filter(lambda x: x != '\n', file.readlines()))
            groups = list(map(lambda x: x if x[-2] == 'o' or x[-2] == 'p' else x[:x.rfind(' ')] + '\n', groups))
            with open(f"Pools/{item}", "w", encoding="utf-8") as file:
                file.writelines(groups)

    session = vk_api.VkApi(token=active_tokens[0])
    vk = session.get_api()
    account_counter = 0
    all_deleted = []
    for i in range(len(paths)):
        with open(f"Pools/{paths[i]}", encoding="utf-8") as file:
            groups = list(filter(lambda x: x != '\n', file.readlines()))
        if current_post_send_counter[indexes[i]] >= len(groups):
            print(f"\n\t{paths[i][:-4].replace('_', ' ')} ({len(groups)}):\n")
            print("\tВсе посты опубликованы!")
            continue
        new_groups = groups[:current_post_send_counter[indexes[i]]]
        for j in range(len(groups)):
            groups[j] = groups[j][:-1]
        ids = list(map(lambda x: int(x[:x.find(' ')]), groups))
        followers = list(map(lambda x: x[x.find(' ') + 1:], groups))
        followers = list(map(lambda x: x[x.find(' ') + 1:], followers))
        followers = list(map(lambda x: int(x[:x.find(' ')]), followers))
        lucky = posts_published[tok_nums[account_counter]]
        deleted = [paths[i][:-4]]

        while lucky >= limit_posts[account_counter] or tok_nums[account_counter] in banned:
            account_counter += 1
            if account_counter >= len(active_tokens):
                os.system("cls")
                print("\n\tНа сегодня лимит постов исчерпан, придется подождать до завтра")
                showPools()
                with open("Pools/tech_part/accounts.txt", "w") as file:
                    file.writelines(list(map(lambda x: str(x) + '\n', posts_published)))
                with open("Pools/tech_part/current_post_send_counter.txt", "w") as file:
                    file.writelines(list(map(lambda x: str(x) + '\n', current_post_send_counter)))
                exit(1)
            session = vk_api.VkApi(token=active_tokens[account_counter])
            vk = session.get_api()
            lucky = posts_published[tok_nums[account_counter]]

        print(f"\n\t{paths[i][:-4].replace('_', ' ')} ({len(ids)}):\n")
        for j in range(current_post_send_counter[indexes[i]], len(ids)):
            print(f"\t{j + 1}) club{ids[j]} -> ", end='')
            try:
                post_id = vk.wall.post(owner_id=-ids[j], message=message, attachments=attachments)["post_id"]
                # post_id = 5
            except:
                try:
                    vk.groups.join(group_id=ids[j])
                    post_id = vk.wall.post(owner_id=-ids[j], message=message, attachments=attachments)["post_id"]
                    vk.groups.leave(group_id=ids[j])
                except:
                    print(f"не удалось опубликовать   ({active_token_names[account_counter]})")
                    vk.groups.leave(group_id=ids[j])
                    deleted.append(f"club{ids[j]}")
                    continue
                new_groups.append(f"{groups[j]} {post_id}\n")
                current_post_send_counter[indexes[i]] += 1
                lucky += 1
                distance = 20
                if j + 1 >= 10:
                    distance -= 1
                if j + 1 >= 100:
                    distance -= 1
                spaces = ' ' * (distance - len(str(ids[j])) - len(str(post_id)))
                distance2 = 10
                spaces2 = ' ' * (distance2 - len(str(followers[j])))
                print(f"опубликован после подписки {post_id}{spaces}fol: {followers[j]}{spaces2}(lucky: {lucky})   {active_token_names[account_counter]}")
                posts_published[tok_nums[account_counter]] = lucky
                posts_published[tok_nums[account_counter]] = lucky
                while lucky >= limit_posts[account_counter] or tok_nums[account_counter] in banned:
                    if j == len(ids) - 1 and i == len(paths) - 1:
                        break
                    account_counter += 1
                    if account_counter >= len(active_tokens):
                        print("\n\tНа сегодня лимит постов исчерпан, придется подождать до завтра")
                        with open("Pools/tech_part/accounts.txt", "w") as file:
                            file.writelines(list(map(lambda x: str(x) + '\n', posts_published)))
                        with open("Pools/tech_part/current_post_send_counter.txt", "w") as file:
                            file.writelines(list(map(lambda x: str(x) + '\n', current_post_send_counter)))
                        for k in range(j + 1, len(groups)):
                            new_groups.append(groups[k] + '\n')
                        with open(f"Pools/{paths[i]}", "w", encoding="utf-8") as file:
                            file.writelines(new_groups)
                        if len(deleted) > 1:
                            all_deleted.append(deleted)
                        if all_deleted:
                            print("\n\n\tУдаленные группы")
                            for ad in all_deleted:
                                print(f"\n\t{ad.pop(0).replace('_', ' ')}:")
                                for group in ad:
                                    print(f"\t    {group}")
                        showPools()
                        exit(1)
                    session = vk_api.VkApi(token=active_tokens[account_counter])
                    vk = session.get_api()
                    lucky = posts_published[tok_nums[account_counter]]
            else:
                new_groups.append(f"{groups[j]} {post_id}\n")
                current_post_send_counter[indexes[i]] += 1
                lucky += 1
                distance = 20
                if j + 1 >= 10:
                    distance -= 1
                if j + 1 >= 100:
                    distance -= 1
                spaces = ' ' * (distance - len(str(ids[j])) - len(str(post_id)))
                distance2 = 10
                spaces2 = ' ' * (distance2 - len(str(followers[j])))
                if paths[i] == "p.txt":
                    print("предложен ", end='')
                else:
                    print("опубликован ", end='')
                print(f"{post_id}{spaces}fol: {followers[j]}{spaces2}(lucky: {lucky})   {active_token_names[account_counter]}")
                posts_published[tok_nums[account_counter]] = lucky
                while lucky >= limit_posts[account_counter] or tok_nums[account_counter] in banned:
                    if j == len(ids) - 1 and i == len(paths) - 1:
                        break
                    account_counter += 1
                    if account_counter >= len(active_tokens):
                        print("\n\tНа сегодня лимит постов исчерпан, придется подождать до завтра")
                        with open("Pools/tech_part/accounts.txt", "w") as file:
                            file.writelines(list(map(lambda x: str(x) + '\n', posts_published)))
                        with open("Pools/tech_part/current_post_send_counter.txt", "w") as file:
                            file.writelines(list(map(lambda x: str(x) + '\n', current_post_send_counter)))
                        for k in range(j + 1, len(groups)):
                            new_groups.append(groups[k] + '\n')
                        with open(f"Pools/{paths[i]}", "w", encoding="utf-8") as file:
                            file.writelines(new_groups)
                        if len(deleted) > 1:
                            all_deleted.append(deleted)
                        if all_deleted:
                            print("\n\n\tУдаленные группы")
                            for ad in all_deleted:
                                print(f"\n\t{ad.pop(0).replace('_', ' ')}:")
                                for group in ad:
                                    print(f"\t    {group}")
                        showPools()
                        exit(0)
                    session = vk_api.VkApi(token=active_tokens[account_counter])
                    vk = session.get_api()
                    lucky = posts_published[tok_nums[account_counter]]
            time.sleep(1)
        with open(f"Pools/{paths[i]}", "w", encoding="utf-8") as file:
            file.writelines(new_groups)
        if len(deleted) > 1:
            all_deleted.append(deleted)
    with open("Pools/tech_part/accounts.txt", "w") as file:
        file.writelines(list(map(lambda x: str(x) + '\n', posts_published)))
    with open("Pools/tech_part/current_post_send_counter.txt", "w") as file:
        file.writelines(list(map(lambda x: str(x) + '\n', current_post_send_counter)))
    if all_deleted:
        print("\n\n\tУдаленные группы")
        for ad in all_deleted:
            print(f"\n\t{ad.pop(0).replace('_', ' ')}:")
            for group in ad:
                print(f"\t    {group}")
    print('\n')
    os.system("pause")


def getStatistics():
    global current_post_send_counter
    session = vk_api.VkApi(token=my_token)
    vk = session.get_api()
    os.system("cls")
    pools = []
    paths = []
    index = 0
    for n, item in enumerate(os.listdir("Pools")):
        if item[-4:] != '.txt' or item[:2] == '__':
            continue
        paths.append(item)
        with open(f"Pools/{item}") as file:
            groups = list(filter(lambda x: x != '\n', file.readlines()))
        if current_post_send_counter[index] < len(groups):
            print("\n\tПост опубликован еще не во всех группах\n\t" + post_link)
            input()
            return
        current_post_send_counter[index] = len(groups)
        pools.append(groups)
        index += 1
    if os.path.exists("Pools/copy"):
        shutil.rmtree("Pools/copy")
    os.mkdir("Pools/copy")
    with open("Статистика.txt", "w", encoding="utf-8") as file:
        file.write("На момент " + datetime.now().strftime("%H:%M  %d.%m.%Y") + ':\n\n\nИнформация по пулам')
    index = 0
    step = 10
    postsBefore = 0
    postsAfter = 0
    allViews = 0
    allLikes = 0
    allComments = 0
    allReposts = 0
    wholeText = vk.wall.getById(posts=post_link[post_link.find('wall') + 4:])[0]["text"]
    textFromPost = wholeText[:wholeText.find('\n')]
    if not textFromPost.strip():
        textFromPost = wholeText[:wholeText.find('.')]
    with open("Pools/tech_part/searching_phrase.txt", "w", encoding="utf-8") as file:
        file.write(f"\n      Фраза для поиска поста в функции getStatistics():\n\n      |{textFromPost}|")
    toDeleteNo = []
    commentedPost_links = []
    for i in range(len(pools)):
        index += 1
        shutil.copyfile(f"Pools/{paths[i]}", f"Pools/copy/{paths[i]}")
        print(f"\n{index}) {paths[i][:-4].replace('_', ' ')} ({len(pools[i])}):")
        new_pool = []
        group_ids = list(map(lambda x: int(x[:x.find(' ')]), pools[i]))
        post_ids = list(map(lambda x: int(x[x.rfind(' ') + 1:]), pools[i]))
        screen_names = list(map(lambda x: x[x.find(' ') + 1:], pools[i]))
        screen_names = list(map(lambda x: x[:x.find(' ')], screen_names))
        views = 0
        likes = 0
        comments = 0
        reposts = 0
        for j in range(len(group_ids)):  # группы в пуле
            post = {}
            offset = 0
            print(f"\t{j + 1}. club{group_ids[j]} -> ", end='')
            while True:
                try:
                    posts = vk.wall.get(owner_id=-group_ids[j], count=step, offset=offset)["items"]
                except:
                    print("доступ к стене закрыт")
                    offset = -1
                    break

                if paths[i] == 'p.txt':
                    for p in posts:
                        if textFromPost in p["text"]:
                            post = p
                            break
                    if post or len(posts) == 0 or posts[-1]["id"] < post_ids[j]:
                        break
                else:
                    for p in posts:
                        if p["id"] == post_ids[j]:
                            post = p
                            break
                    if post or len(posts) == 0 or posts[-1]["id"] < post_ids[j]:
                        break
                offset += step

            if offset == -1:  # доступ к стене закрыт
                continue

            if post:
                link = f"https://vk.com/{screen_names[j]}?w=wall{post['owner_id']}_{post['id']}"
                print(f"пост висит  {link}")
                new_pool.append(pools[i][j])
                if "views" in post:
                    views += post["views"]["count"]
                    allViews += post["views"]["count"]
                likes += post["likes"]["count"]
                allLikes += post["likes"]["count"]
                reposts += post["reposts"]["count"]
                allReposts += post["reposts"]["count"]
                comments += post["comments"]["count"]
                allComments += post["comments"]["count"]
                if post["comments"]["count"] > 0:
                    commentedPost_links.append(link)
            else:
                if paths[i] == 'p.txt':
                    new_pool.append(pools[i][j])
                    print("пока не опубликовали")
                else:
                    print("убрали")

        postsBefore += len(pools[i])
        postsAfter += len(new_pool)

        if len(new_pool) != len(pools[i]):
            with open(f"Pools/{paths[i]}", "w", encoding="utf-8") as file:
                file.writelines(new_pool)
                current_post_send_counter[index - 1] = len(new_pool)
            if len(new_pool) == 0:
                os.remove(f"Pools/{paths[i]}")
                toDeleteNo.insert(0, index - 1)
            print(f"\t\tГруппы, удалившие наш пост: {len(pools[i]) - len(new_pool)}")
            print(f"\t\tИзменение размера пула: {len(pools[i])} -> {len(new_pool)}")
        elif paths[i] != 'p.txt':
            print(f"\t\tВсе посты висят! ({len(pools[i])})")

        with open(f"Статистика.txt", "a", encoding="utf-8") as file:
            file.write(f"\n\n{index}) {paths[i][:-4].replace('_', ' ')}  ({len(new_pool)} постов):")
            file.write(f"\n\tпросмотров: {views}\n\tлайков: {likes}\n\tкомментариев: {comments}")
            file.write(f"\n\tрепостов: {reposts}")
    for tdn in toDeleteNo:
        del current_post_send_counter[tdn]
    with open("Pools/tech_part/current_post_send_counter.txt", "w") as file:
        file.writelines(list(map(lambda x: str(x) + '\n', current_post_send_counter)))

    print(f"\n\n\tОбщее число удаленных постов: {postsBefore - postsAfter}\n\tИзменение размера пулов: {postsBefore} -> {postsAfter}")
    with open(f"Статистика.txt", "a", encoding="utf-8") as file:
        file.write(f"\n\n\nОбщая статистика ({postsAfter} постов):\n\tпросмотров: {allViews}\n\tлайков: {allLikes}\n\tкомментариев: {allComments}\n\tрепостов: {allReposts}\n\n")
        file.write(f"Ссылки на посты с комментариями:")
        for cpl in commentedPost_links:
            file.write(f"\n    {cpl}")
        file.write("\n\n")
    print("\n\tПолная информация находится в текстовом файле \"Статистика\"")
    input()


def changePostLink():
    global post_link, current_post_send_counter
    os.system("cls")
    if post_link:
        print(f"\n\tТекущая ссылка на пост:\n\t{post_link}")
    while True:
        link = input("\n\tВведи новую ссылку на пост или нажми <enter> для выхода => \n\t")
        link = link.strip()
        if link == "":
            return post_link
        if "wall" not in link:
            print("\tВ ссылке на пост должно быть слово \"wall\"")
        else:
            if post_link != link:
                for i in range(len(current_post_send_counter)):
                    current_post_send_counter[i] = 0
                with open("Pools/tech_part/mailing_date.txt", "w", encoding="utf-8") as file:
                    file.write(datetime.now().strftime("%d.%m.%Y"))
                post_link = link
            break
    with open("Pools/tech_part/post_link.txt", "w") as file:
        file.write(post_link)


def showPools(endProgram=False):
    global current_post_send_counter
    print('\n')
    groups_counter = 0
    nPostPublished = 0
    spaces = []
    for n, item in enumerate(os.listdir("Pools")):
        if item[-4:] != '.txt' or item[:2] == '__':
            continue
        spaces.append(len(item) - 4)
    longestSpace = max(spaces) + 4
    index = 0
    for n, item in enumerate(os.listdir("Pools")):
        if item[-4:] != '.txt' or item[:2] == '__':
            continue
        with open(f"Pools/{item}") as file:
            groups = list(filter(lambda x: x != '\n', file.readlines()))
        groups_counter += len(groups)
        print(f"\t{item[:-4].replace('_', ' ')}{' ' * (longestSpace - spaces[index])}опубликовано: ", end='')
        if current_post_send_counter[index] < len(groups):
            print(str(current_post_send_counter[index]) + ' из ' + str(len(groups)))
        else:
            print("всё")
            if current_post_send_counter[index] > len(groups):
                current_post_send_counter[index] = len(groups)
                with open("Pools/tech_part/current_post_send_counter.txt", "w") as file:
                    file.writelines(list(map(lambda x: str(x) + '\n', current_post_send_counter)))
        nPostPublished += current_post_send_counter[index]
        index += 1
    print(f"\n\tВсего групп: {groups_counter}")
    print(f"\tОпубликовано в: {nPostPublished}")
    print(f"\tОсталось: {groups_counter - nPostPublished}")
    if not endProgram:
        input()


def deleteGroup():
    os.system("cls")
    print("\n\tВведи ссылку на группу, которую нужно удалить: ")
    groupLink = input('\t')
    if "https://" in groupLink:
        groupLink = groupLink[groupLink.rfind('/') + 1:]
    if groupLink.strip() == '':
        return
    for n, item in enumerate(os.listdir("Pools")):
        if item[-4:] != '.txt' or item[:2] == '__':
            continue
        with open(f"Pools/{item}") as file:
            groups = list(filter(lambda x: x != '\n', file.readlines()))
        deleted = False
        for group in groups:
            if groupLink in group:
                groups.remove(group)
                with open(f"Pools/{item}", "w", encoding="utf-8") as file:
                    file.writelines(groups)
                deleted = True
                break
        if deleted:
            print("\n\tГруппа удалена!\n\tНажми enter для возврата в главное меню")
            input()
            return
    print("\n\tТакое группы нет. Возможно, она уже была удалена во время сбора статистики\n\tНажми enter для возврата в главное меню")
    input()


def checkAccounts():
    global tokens, banned
    ok = 0
    ban_tokens = ""
    for i in range(len(tokens)):
        try:
            result = requests.get(f"https://api.vk.com/method/users.get?access_token={tokens[i]}&v={V}").json()
            if "error" in result:
                banned.append(i)
                if ban_tokens:
                    ban_tokens += ', '
                ban_tokens += str(token_names[i])
            else:
                ok += 1
        except requests.exceptions.ConnectionError:
            print("Нет интернета")
            exit(0)
    if len(banned) > 0:
        ban_tokens = " (" + ban_tokens + ")" if ban_tokens else ""
        answer = f"Внезапная проверка аккаунтов:\nдействующих: {ok}\nзабаненных: {len(banned)}{ban_tokens}"
        requests.get(f"https://api.vk.com/method/messages.send?user_id={my_id}&message={answer}&random_id=0&access_token={helper_token}&v={V}")


def cantPublishAnymore():
    for i in range(len(posts_published)):
        if posts_published[i] != -1 and posts_published[i] < limit_posts[i]:
            return False
    return True


def pickUpRightWordEnding(number, ones: str, two_three_four: str, rest: str, writeNumber1=True):
    phrase = f"{number} "
    if not writeNumber1 and number == 1:
        phrase = ''
    if number % 10 == 1 and number % 100 != 11:
        phrase += ones
    elif (number % 10 == 2 or number % 10 == 3 or number % 10 == 4) and not (12 <= number % 100 <= 14):
        phrase += two_three_four
    else:
        phrase += rest
    return phrase


def createTechPartIfNotExist():
    if not os.path.exists("Pools/tech_part"):
        os.mkdir("Pools/tech_part")
        with open("Pools/tech_part/accounts.txt", "w") as file:
            for _ in range(len(tokens)):
                file.write('0\n')
        with open("Pools/tech_part/current_post_send_counter.txt", "w") as file:
            pools_amount = 0
            for item in os.listdir("Pools"):
                if len(item) >= 4 and item[-4:] == '.txt' and item[:2] != '__':
                    pools_amount += 1
            for _ in range(pools_amount):
                file.write('0\n')
        open("Pools/tech_part/post_link.txt", 'x')


if __name__ == '__main__':
    createTechPartIfNotExist()
    with open("Pools/tech_part/post_link.txt") as f:
        post_link = f.readline()
    main()
