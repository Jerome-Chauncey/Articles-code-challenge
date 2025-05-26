from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, validates
from lib.models.base import Base
from lib.models.association import author_magazine
from lib.models import db

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
    
    def author(self):
        from models import Author, Article
        return (
            Author.query.join(Article).filter(Article.magazine_id == self.id).distinct().all()
        )
    
    @classmethod
    def multiple_authors(cls):
        from models import Article
        return (
            cls.query.join(Article).group_by(Article.magazine_id).having(db.func.count(db.func.distinct(Article.author_id)) >= 2).all()
        )
    @classmethod
    def article_counts(cls):
        from models import Article
        return (
            db.session.query(cls.name, db.func.count(Article.id).label('article_count')).outerjoin(Article).group_by(cls.id).all()
        )
    
    
        