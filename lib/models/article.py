from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from lib.models.base import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"))
    magazine_id = Column(Integer, ForeignKey("magazines.id"))

    author = relationship("Author", back_populates="articles")
    magazine = relationship("Magazine", back_populates="articles")