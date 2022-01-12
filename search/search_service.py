from datetime import datetime

import bs4
import json
import os
import redis
import re
import requests
import time


REDIS_HOST              = os.environ.get('REDIS_HOST') if os.environ.get('REDIS_HOST') is not None else 'localhost'
redis_client            = redis.Redis(host=REDIS_HOST, port=6379)
REDIS_WAITING_QUEUE     = 'API_SERVICE_SEARCH_WAITING'
REDIS_PROCESSED_QUEUE   = 'API_SERVICE_SEARCH_PROCESSED'
HEADERS                 = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

if __name__ == '__main__':
    while True:
        value = redis_client.rpop(REDIS_WAITING_QUEUE)

        if value is None:
            continue

        print(f'[{datetime.now()}] {value}')
        value = value.decode().replace(" ", "+")
        link = f'https://www.google.com/search?q=steam+{value}'
        req = requests.get(link, headers=HEADERS)
        soup = bs4.BeautifulSoup(req.text, 'html.parser')
        names = soup.find_all('div', {'class': 'yuRUbf'})

        for name in names:
            url = name.find('a')['href']
            temp = re.search(r'https://store.steampowered.com/app/(.*)', url)
            if temp:
                keywords = temp.group(1).split('/')
                if len(keywords) != 1:
                    app, name = keywords[0:2]
                    if 'romanian' not in temp.group():
                        data = json.dumps({
                            'value': value,
                            'appid': app,
                            'appurl': temp.group(),
                            'appname': name
                        })
                        redis_client.rpush(REDIS_PROCESSED_QUEUE, data)
        redis_client.rpush(REDIS_PROCESSED_QUEUE, 'FINISHED')
