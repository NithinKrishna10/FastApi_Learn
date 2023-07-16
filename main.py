from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():


    return {"hey": "guys"}


@app.get('/about')
def about():
    return {'data' :{'about page'}}