# Python
from typing import List, Optional

# Pydantic
from pydantic import BaseModel, Field

# FastAPI
from fastapi import Depends, Path, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter

# Config
from config.database import Session

# Models
from models.movie import Movie as MovieModel

# Middlewares
from middlewares.jwt_beares import JWTBearer

# My Router
movie_router = APIRouter()

# Movies Model Pydantic
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15,
                       title="Movie ID", description="This is the movie")
    overview: str = Field(
        min_length=15, max_length=50, title="Movie Overview",
        description="This is the movie overview")
    year: int = Field(ge=1900, le=2021)
    rating: float = Field(ge=0.0, le=10.0)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi pelicula",
                "overview": "Descripcion de mi pelicula ...",
                "year": 2000,
                "rating": 5.0,
                "category": "Acción"
            }
        }

# Routes
@movie_router.get(
    "/movies", tags=["movies"], response_model=List[Movie],
    status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)


@ movie_router.get("/movies/{id}", tags=["movies"], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'No se ha encontrado la pelicula'})
    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
 
@ movie_router.get("/movies/", tags=["movies"], response_model=List[Movie])
def get_movies_by_category(
    category: str = Query(min_length=5, max_length=15,
                          title="Categoria Movie",
                          description="This is the movie category")) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'Not movies in that category'})
    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)


@ movie_router.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session() 
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit() # Save data
    return JSONResponse(content={"message": "se ha registrado la pelicula"}, status_code=201)


@ movie_router.put("/movies", tags=["movies"], response_model=dict, status_code=200)
def update_movie(
        id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'Movie not found'})
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit() # Save
    return JSONResponse(content={"message": "se ha actualizado la pelicula"}, status_code=200)


@ movie_router.delete("/movies", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'Movie not found'})
    db.delete(result)
    db.commit() # Save
    return JSONResponse(content={"message": "se ha eliminado la pelicula"}, status_code=200)