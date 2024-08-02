from fastapi import FastAPI, Request
from starlette.templating import Jinja2Templates

from top_albums.routers import album

app = FastAPI()
templates = Jinja2Templates(directory='templates')

app.include_router(album.router)


@app.get('/')
def read_root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})
