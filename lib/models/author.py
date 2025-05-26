# lib/models/author.py
from lib.models.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, validates

from lib.models.association import author_magazine
from lib.models import db





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
    
    def articles(self):
        return self.articles
    
    def magazines(self):
        from models import Magazine, Article
        return(
            Magazine.query.join(Article).filter(Article.author_id == self.id).distinct().all()


        )
    
    def top_author(cls):
        from models import Article
        return (
            db.session.query(cls, db.func.count(Article.id).label("article_count")).join(Article).group_by(cls.id).order_by(db.desc("article_count")).first()
        )
    







