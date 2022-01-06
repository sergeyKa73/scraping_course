import requests
import lxml
from bs4 import BeautifulSoup

def get_html(url):
    r = requests.get(url)
    return r.text

def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    h1 = soup.find('div', id='content').find('h1').text
    return h1


def main():
    url = 'https://modx.ru/o-sisteme-modx/modx-revolution/'
    print(get_content(get_html(url)))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

