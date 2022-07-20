from bs4 import BeautifulSoup as bs
import requests

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

BASE_URL = 'https://habr.com/ru/all/'
START_URL = 'https://habr.com'

HEADERS = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}


def get_soup(url):
    ses = requests.Session()
    response = ses.get(url=url, headers=HEADERS)
    return bs(response.text, 'html.parser')


def get_text_article(article):
    list_text = article.find('div', class_='article-formatted-body').contents
    text = ''
    for el in list_text:
        text += str(el)
    return text.lower()


def parse():
    soup = get_soup(BASE_URL)
    articles = soup.find_all("div", class_="tm-article-snippet")
    list_of_articles = []

    for article in articles:
        alink = article.find('a', class_='tm-article-snippet__title-link')

        date = article.find('time')['title']

        head = alink.string
        href = alink['href']
        full_link = f'{START_URL}{href}'
        text = get_text_article(article)

        art_soup = get_soup(full_link)
        art_text = get_text_article(art_soup)

        for word in KEYWORDS:
            l_word = word.lower()
            if l_word in head.lower() or l_word in text or l_word in art_text:
                t_el = f'<{date}> - <{head}> - <{full_link}>'
                if t_el not in list_of_articles:
                    list_of_articles.append(t_el)

    return list_of_articles


if __name__ == '__main__':
    list_of_articles = parse()
    for el in list_of_articles:
        print(el)
