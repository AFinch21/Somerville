from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from typing import List
import os

Base = declarative_base()

def get_db():
    # Example setup (if you are using PostgreSQL)
    DATABASE_URL = os.environ.get('DATABASE_URL')
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

    # Connect to the database
    connection = engine.connect()

    # Close the connection
    connection.close()
    
    return engine
