# Pydantic
from pydantic import BaseModel, Field

# FastAPI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from jwt_manager import create_token
from fastapi import APIRouter

# Config
from config.database import Session, engine, Base

# Routers
from routers.movie import movie_router

# My Router
user_router = APIRouter()

# User Model Pydantic
class User(BaseModel):
    email: str = Field(min_length=5, max_length=100,
                       title="Email",
                       description="This is the email")
    password: str = Field(min_length=5, max_length=15,
                          title="Password",
                          description="This is the password")


# POST: LOGIN USER
@user_router.post("/login", tags=["user"], response_model=dict, status_code=200)
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(content=token, status_code=200)
    return JSONResponse(content={"message": "usuario o contraseña incorrectos"}, status_code=401)