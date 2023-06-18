from datetime import datetime
# import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

class Main():

    def __init__(self):
        pass

    def __crawl(self):
        url = f'http://www.ucc-cinema.com.tw/main02.asp'
        print(f"crawl url: {url}")

        r = requests.get(url)
        r.encoding = 'big5'
        # soup = BeautifulSoup(r.text, "lxml")
        soup = BeautifulSoup(r.text, 'html.parser')

        movie_title = []
        info_bricks = soup.findAll("table", width='100%', border = 0, bgcolor = '#333333')
        for info_brick in info_bricks:
            title_brick = info_brick.findAll("font", size='3')[0]
            title_str = list(title_brick)[0]
            title_str = title_str.replace('\t', '')
            movie_title.append(title_str)
        created_at = [datetime.now() for _ in range(len(movie_title))]

        dataset = pd.DataFrame({ 'movie_title': movie_title, 'created_at': created_at })

        return dataset

    def launch(self):
        """
        啟動主程式

        :return: DataFrame
        """
        new_dataset = self.__crawl()
        old_dataset = pd.read_csv('history_movie_title.csv', index_col=0)
        dataset = pd.concat([new_dataset, old_dataset], axis=0, ignore_index=True)
        dataset.to_csv('history_movie_title.csv')

        return dataset
