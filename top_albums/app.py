from fastapi import FastAPI

from top_albums.routers import album

app = FastAPI()

app.include_router(album.router)


@app.get('/')
def read_root():
    return {'message': 'hello world'}
