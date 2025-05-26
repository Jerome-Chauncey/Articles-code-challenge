# lib/models/author.py
from lib.models.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, validates

from lib.models.association import author_magazine





class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    articles = relationship("Article", back_populates="author")
    magazines = relationship("Magazine", secondary=author_magazine, back_populates="authors")

    def __repr__(self):
        return f"<Author(name='{self.name}')>"

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Author name cannot be empty")
        return value






