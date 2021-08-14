import uvicorn

from app.main import get_app

app = get_app()

if __name__ == "__main__":
    uvicorn.run("app.__main__:app", reload=True)
