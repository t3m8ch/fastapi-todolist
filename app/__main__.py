import uvicorn
from fastapi import FastAPI

from app.endpoints import include_routers

app = FastAPI()
include_routers(app)


if __name__ == '__main__':
    uvicorn.run("app.__main__:app", reload=True)
