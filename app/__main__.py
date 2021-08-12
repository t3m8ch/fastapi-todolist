import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Hello!"}


if __name__ == '__main__':
    uvicorn.run("app.__main__:app", reload=True)
