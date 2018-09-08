'''
author: xiche
create at: 08/24/2018
description:
    Spider for Douban
Change log:
Date        Author      Version    Description
08/24/2018  xiche       1.0        Top n Movies of Spider for Douban
08/28/2018  xiche       1.1        refactor the code
'''
import requests
import os
import codecs
import re
from contextlib import closing
from bs4 import BeautifulSoup
from abc import abstractmethod, ABC

class Spider(ABC):
    url_request = ''
    html = ''
    HEADER_BROWER = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
            'Chrome/63.0.3239.132 Safari/537.36'}

    def download_page(self):
        data = requests.get(self.url_request, headers=self.HEADER_BROWER).text
        self.html = data
        return data

    @abstractmethod
    def parse_html(self, html):
       pass

    @abstractmethod
    def start_spider(self):
        pass

    def getPic(self, data):
        pic_list = re.findall(r'src="http.+?.jpg"', data)
        return pic_list

    def download_pic(self, url, name, folder = 'imgs/'):
        rootPath = folder
        if not os.path.exists(rootPath):
            os.makedirs(rootPath)
        response = requests.get(url, stream=True)
        pic_type = '.' + url.split('.')[-1]
        with closing(requests.get(url, stream=True)) as responses:
            with open(rootPath + name + pic_type, 'wb') as file:
                for data in response.iter_content(128):
                    file.write(data)

class SpiderDouban250(Spider):
    start = 0
    page  = 2
    movies_list_total = []
    def __init__(self, page=2):
        self.page = page
    def parse_html(self, html=None):
        html = html if html else self.html
        soup = BeautifulSoup(html, "html.parser")
        movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})
        movie_name_list = []
        for movie_li in movie_list_soup.find_all('li'):
            detail = movie_li.find('div', attrs={'class': 'hd'})
            movie_name = detail.find('span', attrs={'class': 'title'}).getText()
            score = movie_li.find('div', attrs={'class': 'bd'})
            movie_score = score.find('span', attrs={'class': 'rating_num'}).getText()
            movie_detail = "{}({})".format(movie_name , movie_score)
            movie_name_list.append(movie_detail)

        next_page = soup.find('span', attrs={'class': 'next'}).find('a')
        if next_page:
            return movie_name_list, self.url_request + next_page['href']
        return movie_name_list, None

    def start_spider(self):
        start = self.start
        movies_list_total = []
        while(start < 25 * self.page):
            self.url_request = 'https://movie.douban.com/top250?self.start={}'.format(start)
            self.download_page()
            picdata = self.getPic(self.html)
            movies, url = self.parse_html()
            movies_list_total = movies_list_total + movies
            index_movies = 0
            for picinfo in picdata:
                self.download_pic(picinfo[5:-1], 'Top' + str(index_movies+1) + '-' + movies[index_movies])
                print(movies[index_movies] + ' download finished')
                index_movies += 1
                start += 1
        with codecs.open('movies.txt', 'w', encoding='utf-8') as fp:
            fp.write(u'\r\n'.join(movies_list_total))

if __name__ == '__main__':
    spider_douban = SpiderDouban250(2)
    spider_douban.start_spider()
   
