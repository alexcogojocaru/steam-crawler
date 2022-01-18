from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

import json
import requests
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory='templates/')

@app.get('/')
async def hekki(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})

@app.post('/search')
async def search_games(request: Request, gameparams: str = Form(...)):
    gameparams = gameparams.split(' ')
    req = requests.post('http://localhost:4000/api/gamecode', json=gameparams)
    return templates.TemplateResponse('listing.html', context={'request': request, 'data': req.json()})

@app.get('/game/{appid}')
async def get_game_stats(appid: int):
    req = requests.get(f'http://localhost:4000/api/game/{appid}')
    return req.json()

if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8080, reload=True)