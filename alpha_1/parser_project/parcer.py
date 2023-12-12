from bs4 import BeautifulSoup as bs
import requests
import fake_useragent
import logging

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")

class Parser:

    def __init__(self, request, page: int = None):
        self.url = 'https://www.chitai-gorod.ru/search'
        self.user_agent = fake_useragent.UserAgent()
        self.user = self.user_agent.random
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': str(self.user),
            'Accept-Language': 'ru'
        }
        params = {
            'phrase': request,
            'filters[categories]': 18030,
        }
        if page and page > 1:
            params['page'] = page
        r = self.session.get(self.url, params=params, headers={'User-Agent': str(self.user)})
        self.html = r.text
        soup = bs(self.html, 'lxml')
        pages = []
        number = 1
        try:
            number_pages = (soup.find('section').
                     find('div', class_='pagination').find('div', class_='pagination__wrapper').
                     find_all('div', class_='pagination__button'))
            for i in number_pages[:-1]:
                pages.append(i.find('span', class_='pagination__text').get_text(strip='\n'))
        except Exception:
            logging.error(f"Страница по запросу {request} не найдена")
        if (len(pages) != 0) :
            number = int(pages[-1])
        self.html_list = []
        self.html_list.append(self.html)
        if number > 1:
            for i in range(1, number):
                params['page'] = i
                r = self.session.get(self.url, params=params, headers={'User-Agent': str(self.user)})
                self.html_list.append(r.text)


    def get_html_by_link(self, url):
        user_agent = fake_useragent.UserAgent()
        user = user_agent.random
        session = requests.Session()
        session.headers = {
            'User-Agent': str(user),
            'Accept-Language': 'ru'
        }
        r = session.get(url, headers={'User-Agent': str(user)})
        return r.text

    def all_links(self):
        all_links = []
        for html in self.html_list:
            soup = bs(html, 'lxml')
            ads = ''
            try:
                ads = soup.find('div', class_='products-list').find_all('div', class_='product-card__text product-card__row')
            except Exception:
                logging.error("Страница по запросу не найдена")
            for ad in ads:
                link = 'https://www.chitai-gorod.ru' + ad.find('a', class_='product-card__title').get('href')
                all_links.append(link)
        return all_links

    def get_page_data(self, html, url):
        soup = bs(html, 'lxml')
        try:
            title = (soup.find('div', class_='product-page__content__product')
                     .find("div", class_='product-info-area product-page__info-container')
                     .find('div', class_='product-detail-title').find('h1')
                     .get_text(strip='\n'))
        except Exception:
            title = 'Нет информации о названии'
        try:
            author = (soup.find("div", class_='product-info-area product-page__info-container')
                      .find('div', class_='product-detail-title')
                      .find('div', class_='product-detail-title__authors')
                      .get_text(strip='\n'))
        except Exception:
            author = 'Нет информации об авторе'
        try:
            price = (soup.find('div', class_='product-detail-offer product-page__offer')
                     .find('div', class_='product-detail-offer-header__price')
                     .find('span')
                     .get_text(strip='\n'))
        except Exception:
            price = 'Нет информации о цене'
        year_release = 'Нет информации о годе издания'
        pages = 'Нет информации о количестве страниц'
        try:
            product_detail_characteristics = (soup.find('div', class_='product-detail-info__characteristics-wrapper')
                                              .find('div', class_='product-detail-characteristics')
                                              .find_all('div', class_='product-detail-characteristics__item'))
            publishing = 'Нет информации об издательстве'
            year_release = 'Нет информации о годе издания'
            for i in product_detail_characteristics:
                if 'Издательство' in i.text:
                    publishing = i.find('a').get_text(strip='\n')
                    continue
                if 'Год издания' in i.text:
                    year_release = i.find('span', itemprop='datePublished').get_text(strip='\n')
                    continue
                if 'Количество страниц' in i.text:
                    pages = i.find('span', itemprop='numberOfPages').get_text(strip='\n')
                    continue
        except Exception:
            publishing = 'Произошли изменения в характеристиках, нужны правки кода'
        try:
            description = (soup.find('div', class_='product-description-area product-page__additional')
                           .find('div', itemprop='description')
                           .text.strip('\r.')
                           .replace('\xa0', ' '))
        except Exception:
            description = 'ERROR'
        data = {'title': title, 'author': author, 'price': price,
                'publishing': publishing,'year_release': year_release, 'pages': pages, 'description': description, 'url': url}
        return data


def parcer_start(title):

    start = Parser(title, page=1)
    all_links = start.all_links()
    cnt_link = len(all_links)
    data = []
    for link in all_links:
        html = start.get_html_by_link(link)
        data.append(start.get_page_data(html, link))
    print(data)
    return data, cnt_link