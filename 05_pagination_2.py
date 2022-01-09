import requests
from bs4 import BeautifulSoup as bs
import fake_useragent
import csv
import re

user = fake_useragent.UserAgent().random
header = {'user-agent': user}
CSV = 'data/books.csv'

def get_html(url):
    r = requests.get(url, headers=header)
    if r.ok:  # 200  ## 403 404
        return r.text
    print(r.status_code)

def refined_price(p):
    r = str(p).split()
    return r[0]

def refined_rating(n):
    return str(n).split('—')[-1]

def write_csv(data, path):
    with open(path, 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['writer'],
                         data['name'],
                         data['rating'],
                         data['url'],
                         data['price']))

def get_page_content(html):
    soup = bs(html, 'lxml')
    books = soup.find_all('div', class_= 'item-type-card__item')
    for book in books:
        link = 'https://oz.by/'
        try:
            writer = book.find('p', class_='item-type-card__info').text

        except:
            writer = ''
        try:
            name = book.find('p', class_='item-type-card__title').text
        except:
            name = ''
        try:
            n = book.find('p', class_='item-type-card__stars').get('title')
            rating = refined_rating(n)
        except:
            rating = ''
        try:
            url = link + book.find('a', class_='item-type-card__link').get('href')
        except:
            url = ''
        try:
            p = book.find('span', class_='item-type-card__btn').text.strip()
            price = refined_price(p)
        except:
            price = ''


        data = {'writer': writer,
                'name': name,
                'rating': rating,
                'url': url,
                'price': price,
                 }

        write_csv(data, CSV)


def main():
    url = 'https://oz.by/books/bestsellers'
    while True:
        get_page_content(get_html(url))

        soup = bs(get_html(url), 'lxml')

        try:
            url = 'https://oz.by/books/bestsellers?page=' + soup.find( 'a', class_="g-pagination__next pg-next").get('data-value')

        except:
            print('Error')

if __name__ == '__main__':
    main()
