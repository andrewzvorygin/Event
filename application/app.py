import uvicorn
from fastapi import FastAPI

from application.api import main_router

from application.settings import api_settings

app = FastAPI()
app.include_router(main_router)


if __name__ == '__main__':
    uvicorn.run('app:app', host=api_settings.host, port=api_settings.port)
