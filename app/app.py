from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

import requests
import bs4
import re
import json
import redis
import os
import uvicorn

HEADERS                 = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
REDIS_WAITING_QUEUE     = 'API_SERVICE_SEARCH_WAITING'
REDIS_PROCESSED_QUEUE   = 'API_SERVICE_SEARCH_PROCESSED'
REDIS_HOST              = os.environ.get('REDIS_HOST') if os.environ.get('REDIS_HOST') is not None else 'localhost'

app = FastAPI()
redis_client = redis.Redis(host=REDIS_HOST, port=6379)

def get_data(data, element, classname, pattern):
    soup = bs4.BeautifulSoup(data, 'html.parser')
    searchdata = str(soup.find_all(element, { 'class': classname })[0])

    value = re.search(pattern, searchdata)
    return value.group(1).split(' ')[0]

@app.post('/api/gamecode')
async def get_urls(keywords: List[str]):
    for key in keywords:
        redis_client.rpush(REDIS_WAITING_QUEUE, key)

    cache, search = {}, 0
    print(search)
    while search != len(keywords):
        value = redis_client.rpop(REDIS_PROCESSED_QUEUE)

        if value:
            value = value.decode()
            if value == 'FINISHED':
                search += 1
                continue

            link = json.loads(value)
            keyword = link['value']
            if keyword not in cache:
                cache[keyword] = [link]
            else:
                cache[keyword].append(link)

    return cache

@app.get('/api/game/{appid}')
async def get_game(appid: str):
    req = requests.get(f'https://steamcommunity.com/app/{appid}', headers=HEADERS)

    try:
        players_ingame = get_data(req.text, 'span', 'apphub_NumInApp', r'<span class="apphub_NumInApp">(.*)</span>')
    except:
        return 'INVALID_APP_ID'

    try:
        original_price      = get_data(req.text, 'div', 'discount_original_price', r'<div class="discount_original_price">(.*)</div>')
        discounted_price    = get_data(req.text, 'div', 'discount_final_price', r'<div class="discount_final_price">(.*)</div>')

        return {
            'players_ingame': players_ingame,
            'original_price': original_price,
            'discounted_price': discounted_price,
            'time': datetime.now().timestamp()
        }
    except:
        price = get_data(req.text, 'div', 'price', r'<div class="price">(.*)</div>')

        return {
            'players_ingame': players_ingame,
            'price': price,
            'time': datetime.now().timestamp()
        }

if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=8000, reload=True)