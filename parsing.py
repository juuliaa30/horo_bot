import requests
from bs4 import BeautifulSoup

def get_capicorn():
    req = requests.get('https://horoscopes.rambler.ru/capricorn/')
    src = req.text

    soup = BeautifulSoup(src, 'html.parser')

    title = soup.find('p', 'UqoHt aTWfO')
    return title.text