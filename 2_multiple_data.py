import requests
import csv
from bs4 import BeautifulSoup

def get_html(url):
    r = requests.get(url)
    return r.text

def write_csv(data):
    with open('plagin.csv', 'a') as file:
        writer = csv.writer(file)

        writer.writerow((data['name'],
                         data['url'],
                         data['info']))

def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    cards = soup.find('div', class_='row text-center')
    plagins = cards.find_all('div', class_='card-body')
    cards_info = []

    for plagin in plagins:
        name = plagin.find('h3', class_='h6').text,
        link =  str('https://modx.com/' + plagin.find('a', class_='stretched-link').get('href')),
        info =  plagin.find('p', class_='text-muted').text

        data = {
            'name': name,
            'url': link,
            'info': info
        }

        #print(data)
        write_csv(data)

def main():
    url = 'https://modx.com/extras/'
    get_content(get_html(url))

if __name__ == '__main__':
    main()