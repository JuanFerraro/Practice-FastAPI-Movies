#Python
import os

# SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base # Manipulate database tables

# DataBase name
sqlite_file_name = "database.sqlite"

# Read actual file (database.py)
base_dir = os.path.dirname(os.path.realpath(__file__)) 

# Create DataBase URL
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

# Create DataBase Engine
engine = create_engine(database_url, echo=True)

# Create Session
Session = sessionmaker(bind=engine)

# Create a Instance
Base = declarative_base()