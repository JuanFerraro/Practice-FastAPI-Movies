# SQLAlchemy
from sqlalchemy import Column, Integer, String, Float

# DataBase
from config.database import Base

class Movie(Base): # DataBase Entity

    __tablename__="movies"

    id = Column(Integer, primary_key= True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)