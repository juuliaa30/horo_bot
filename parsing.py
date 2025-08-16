import requests
from bs4 import BeautifulSoup

def get_horo(text):
    try:
        req = requests.get(f'https://horoscopes.rambler.ru/{text}/')
        src = req.text

        soup = BeautifulSoup(src, 'html.parser')

        article = soup.find('div', itemprop="articleBody")
        if article:
            horo_text = article.find('p').text
            return horo_text

    except Exception as e:
        return f"Ошибка {e}"