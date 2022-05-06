import requests

fincult = 'https://fincult.info/api/v1/articles'
ses = requests.Session()


def replase_non_printed_char(i_str):
    non_printed_chars = ['\u200b', '\xd7']
    for char in non_printed_chars:
        i_str = i_str.replace(char, '')
    return i_str

def get_article_text(article):
    article_url = f'{fincult}/item/{article}'
    response = ses.get(article_url)

    start_url = 'https://fincult.info/'

    if response.status_code == 200:
        of = open(f'.\{article}.txt', 'w')
        data = response.json()
        name = replase_non_printed_char(data["name"])
        of.write(name + '\n')
        description = replase_non_printed_char(data["description"])
        of.write(description + '\n')
        for el in data["content"]:
            if el["code"] == "text":
                data_title = replase_non_printed_char(el["data"]["title"])
                of.write(data_title + '\n')
                data_text = replase_non_printed_char(el["data"]["text"])
                of.write(data_text + '\n')
                image = el["data"].get("image")
                if image != None:
                    src = image["file"]["src"]
                    p = requests.get(f'{start_url}{src}')
                    # руками создать папку img в папке с проектом
                    img_path = f'.\img\{src.replace("/", "_")}'
                    out = open(img_path, 'wb')
                    out.write(p.content)
                    out.close()
                    of.write(img_path + '\n')
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
