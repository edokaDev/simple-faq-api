from sqlmodel import create_engine
from sqlmodel import Session
from settings import DB_URL

engine = create_engine(DB_URL, echo=True)
session = Session(bind=engine)
