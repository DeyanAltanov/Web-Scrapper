import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy
import re

r = r"[a-zA-Z0-9\-\_\/\.]+\.html"
pages = numpy.arange(1, 51, 1)
book_title = []
book_upc = []
book_type = []
book_price = []
book_availability = []

for page in pages:
    url = 'https://books.toscrape.com/catalogue/page-' + str(page) + '.html'

    results = requests.get(url)

    soup = BeautifulSoup(results.text, 'html.parser')

    book_div = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

    for container in book_div:
        book_url_extract = str(container.article.find('div', class_='image_container').a)
        bu_regex = re.findall(r, book_url_extract)
        book_url = 'https://books.toscrape.com/catalogue/' + bu_regex[0]
        book_url_results = requests.get(book_url)
        book_soup = BeautifulSoup(book_url_results.text, 'html.parser')
        info = book_soup.article.find('table', class_='table table-striped')
        title = container.article.h3.a['title']
        book_info = info.find_all('td')
        upc = (str(book_info[0])[4:][:-5])
        type = (str(book_info[1])[4:][:-5])
        price = (str(book_info[2])[5:][:-5])
        availability = (str(book_info[5])[14:][:-16])

        book_title.append(title)
        book_upc.append(upc)
        book_type.append(type)
        book_price.append(price)
        book_availability.append(availability)

col_dict = {'title': book_title, 'upc': book_upc, 'type': book_type, 'price': book_price, 'availability': book_availability}
book_store = pd.DataFrame(col_dict)

book_store.to_csv('report.csv')