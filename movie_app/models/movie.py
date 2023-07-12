#SQLAlchemy
from sqlalchemy import Column

# DataBase
from config.database import Base

class Movie(Base): # DataBase Entity

    __tablename__="movies"

    id = Column