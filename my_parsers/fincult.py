import requests

fincult = 'https://fincult.info/api/v1/articles'
ses = requests.Session()


def get_article_text(article):
    article_url = f'{fincult}/item/{article}'
    response = ses.get(article_url)

    if response.status_code == 200:
        of = open(f'.\{article}.txt', 'w')
        data = response.json()
        of.write(data["name"] + '\n')
        of.write(data["description"].replace('\u200b', '') + '\n')
        for el in data["content"]:
            if el["code"] == "text":
                of.write(el["data"]["title"]  + '\n')
                of.write(el["data"]["text"].replace('\xd7', '') + '\n')
        of.close()


def get_articles():
    ses = requests.Session()

    response = ses.get(fincult)

    if response.status_code == 200:
        data = response.json()
        count = 0
        for article in data:
            if count == 10:
                break
            get_article_text(article["code"])
            count += 1

get_articles()
