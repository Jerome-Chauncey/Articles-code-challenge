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
    

    def articles(self):
        result = db.session.execute(
            """
                SELECT * FROM articles WHERE magazine_id = :magazine_id
            """,
            {"magazine_id: self.id"}
        )
        return result.fetchall()
    

    def contributors(self):
        result = db.session.execute(
            """
                SELECT DISTINCT authors.* FROM authors
                JOIN articles ON authors.id = articles.author_id
                WHERE articles.magazine_id = :magazine_id
            """,
            {"magazine_id": self.id}
        )
        return result.fetchall()
    
    def article_titles(self):
        result = db.session.execute(
            """
            SELECT title FROM articles WHERE magazine_id = :magazine_id  
            """,
            {"magazine_id": self.id}
        )
        return [row[0] for row in result.fetchall()]
    
    def contributing_authors(self):
        result = db.session.execute(
            """
            SELECT authors. * FROM authors
            JOIN articles ON authors.id = articles.author_id 
            WHERE articles.magazine_id = :magazine_id
            GROUP BY authors.id
            HAVING COUNT(articles.id) > 2 
            """
        )
        return result.fetchall()
        