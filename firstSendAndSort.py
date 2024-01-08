
# из папки "raw" берем id групп, пробуем опубликовать пост с основных страниц (скорей всего будет много жалоб с первой
# проходки, тк есть много групп, не подходящих по тематике, но среди них много закрытых групп, поэтому уйдет слишком
# много времени чтобы просмотреть все с помощью проги на c++)

# делее пробуем опубликовать пост в каждой из групп. Будет 3 варианта развития событий:
#   - пост опубликуется (проверка по id поста среди предложенных постов группы: его там не будет) - записываем инфу
#        "{id} {screen_name} {fols_amount} o {post_id}" в файл "Pools/{название пула}.txt"
#   - пост не опубликуется, но попадет в предложку (функция не вернет ошибки, но пост будет среди предложенных постов
#       группы) - записываем инфу "{id} {screen_name} {fols_amount} p {post_id}" в файл "Pools/p/{название пула}__p.txt"
#   - пост не опубликуется никуда

# задаем вручную post_link, current_file, startFrom, lucky и index

import requests
from data import my_token, t3, V
import os
from time import sleep
dima_token = t3

tokens = [my_token]
token_names = ["Тимофей"]

post_link = ''

obj = post_link[post_link.find("wall"):]  # для репоста
owner_id_and_post_id = post_link[post_link.find('wall') + 4:]
url = f"https://api.vk.com/method/wall.getById?posts={owner_id_and_post_id}&access_token={dima_token}&v={V}"
message = ''
attachment = ''
try:
    src = requests.get(url).json()["response"][0]
    message = src["text"]
    for attach in src["attachments"]:
        if attach["type"] == "link" and "://" in attachment:
            continue
        if attachment != "":
            attachment += ','
        if attach["type"] == "link":
            attachment += attach["link"]["url"]
        else:
            attachment += attach["type"] + str(attach[attach["type"]]["owner_id"]) + '_' + str(attach[attach["type"]]["id"])
except:
    print("походу Димана забанили\n")
    exit(-1)

# для проверки
# url = f"https://api.vk.com/method/wall.post?owner_id=-215267285&message={message}&attachments={attachment}&access_token={my_token}&v={V}"
# # url = f"https://api.vk.com/method/wall.repost?group_id=215267285&message=Сопроводительный текст&object=wall-216445351_20&access_token={my_token}&v={V}"
# post_id = requests.get(url).json()["response"]["post_id"]
# print(post_id)

current_file = ""  # без '.txt'
startFrom = 0
lucky = 0  # успешные отправки
index = 0  # индекс текущего токена в списке tokens

oneTime = True
if not os.path.exists("Pools/p"):
    os.mkdir("Pools/p")
with open(f"Pools/raw/{current_file}.txt") as file:
    ids = file.readlines()
ids = list(filter(lambda x: x != '\n', ids))
ids = list(map(int, ids))
print(f"\n\t{current_file.replace('_', ' ')}:  ({len(ids)})\n")
for i in range(startFrom, len(ids)):
    current_token = tokens[index]
    print(f"\t{i}) club{ids[i]} - ", end='')
    if lucky == 60 and oneTime:  # после 60 часто перестает публиковать, хотя лимит 100 в день
        oneTime = False
        sleep(10)
    try:
        post_id = requests.get(f"https://api.vk.com/method/wall.post?owner_id=-{ids[i]}&message={message}&attachment={attachment}&access_token={current_token}&v={V}").json()["response"]["post_id"]
        # post_id = requests.get(f"https://api.vk.com/method/wall.repost?group_id={ids[i]}&object={obj}&access_token={tokens[index]}&v={V}").json()["response"]["post_id"]
    except:
        print("нет")
        continue
    else:
        lucky += 1
        try:
            members = requests.get(f"https://api.vk.com/method/groups.getMembers?group_id={ids[i]}&access_token={current_token}&v={V}").json()
            followers = members["response"]["count"]
        except:
            followers = -1
        group = requests.get(f"https://api.vk.com/method/groups.getById?group_id={ids[i]}&access_token={current_token}&v={V}").json()
        screen_name = group["response"][0]["screen_name"]
        post = requests.get(f"https://api.vk.com/method/wall.get?owner_id=-{ids[i]}&filter=suggests&count=1&access_token={current_token}&v={V}").json()
        if len(post["response"]["items"]) == 0:  # пост сразу опубликован
            with open(f"Pools/{current_file}.txt", "a", encoding="utf-8") as file:
                file.write(f"{ids[i]} {screen_name} {followers} o {post_id}\n")
            print(f"опубликован (fol: {followers})\t\tlucky: {lucky}\t<<{token_names[index]}, {index}>>")
        else:  # пост предложен
            with open(f"Pools/p/{current_file}__p.txt", "a", encoding="utf-8") as file:
                file.write(f"{ids[i]} {screen_name} {followers} p {post_id}\n")
            print(f"предложен (fol: {followers})\t\tlucky: {lucky}\t<<{token_names[index]}, {index}>>")
    if lucky % 100 == 0:
        lucky = 0
        index += 1
        if index >= len(tokens):
            print("\n\tЗакончились страницы, на сегодня пожалуй все")
            exit(0)
