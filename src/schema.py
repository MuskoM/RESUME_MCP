from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

from db import engine

Base = declarative_base()


class Posting(Base):
    __tablename__ = "postings"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), index=True)
    url = Column(String(100), unique=True)
    seniority = Column(String(15), index=True)
    tags = Column(String(100))
    scraped_on = Column(DateTime)


Base.metadata.create_all(bind=engine)
