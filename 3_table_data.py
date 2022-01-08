import requests
from bs4 import BeautifulSoup as bs
import fake_useragent
import csv

user = fake_useragent.UserAgent().random
header = {'user-agent': user}


def get_html(url):
    r = requests.get(url, headers=header).text
    return r

def refined(s):
    r = s.split(' ')[0]   # $1,470
    return r.replace('$', '').replace(',', '') # 1470

def write_csv(data):
    with open('cms.csv', 'a') as file:
        writer = csv.writer(file)

        writer.writerow((data['name'],
                         data['symbol'],
                         data['link'],
                         data['price']))

def get_page_data(html):
    soup = bs(html, 'lxml')

    trs = soup.find('table', class_ ='h7vnx2-2 ecUULi cmc-table').find('tbody').find_all('tr')
    url = 'https://coinmarketcap.com'
    for tr in trs:
        tds = tr.find_all('td')
        name = tds[1].text
        symbol = tds[2].find('a').text
        link = url + tds[1].find('a').get('href')
        price = refined(tds[3].text)

        data = {
            'name': name,
            'symbol': symbol,
            'link': link,
            'price': price
        }

        write_csv(data)



def main():
    url = 'https://coinmarketcap.com/exchanges/okex/'
    get_page_data(get_html(url))


if __name__ == '__main__':
    main()
