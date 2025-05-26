# lib/db/connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



engine = create_engine('sqlite:///lib/db/app.db', echo= True)
SessionLocal = sessionmaker(bind=engine)

