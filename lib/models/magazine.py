from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, validates
from lib.models.base import Base
from lib.models.association import author_magazine

class Magazine(Base):
    __tablename__ = "magazines"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)

    articles = relationship("Article", back_populates="magazine")
    authors = relationship("Author", secondary=author_magazine, back_populates="magazines")

    @validates("name", "category")
    def validate_magazine(self, key, value):
        if not value or not value.strip():
            raise ValueError(f"{key.capitalize()} cannot be empty")
        return value
        