# Python
import os

# FastAPI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

# Config
from config.database import Session, engine, Base

# Routers
from routers.movie import movie_router
from routers.users import user_router

# Middlewares
from middlewares.error_handler import ErrorHandler

# My APP! 
app = FastAPI()
app.title = "Mi first app with FatsAPI"
app.version = '0.0.2'

# My Routers
app.include_router(movie_router)
app.include_router(user_router)

# Add Middlewares
app.add_middleware(ErrorHandler)

# 'Create' DB
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

# GET: HOME PATH
@app.get("/", tags=["home"])
def message():
    return HTMLResponse(
        content="""
        <h1>hello world</h1>
        <p>my first api with a content</p>
        """,
        status_code=200)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",
                port=int(os.environ.get("PORT", 8000)))


