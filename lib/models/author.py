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
    


    def magazines_query(self):
        from models import Magazine, Article
        return(
            Magazine.query.join(Article).filter(Article.author_id == self.id).distinct().all()


        )
    
    @classmethod
    def top_author(cls):
        from lib.models.article import Article
        return (
            db.session.query(cls, db.func.count(Article.id).label("article_count"))
            .join(Article)
            .group_by(cls.id)
            .order_by(db.desc("article_count"))
            .first()
        )
    
    def articles_sql(self):
        result = db.session.execute(
            """
                SELECT * FROM articles WHERE author_id = :author_id
            """,
            {"author_id": self.id}
        )
        return result.fetchall()
    
    def magazines_sql(self):
        result = db.session.execute(
            """
                SELECT DISTINCT magazines. * FROM magazine_id
                JOIN articles ON magazines.id = articles.magazine_id
                WHERE articles.author_id = :author_id
            """,
            {"author_id": self.id}
        )
        return result.fetchall()
    
    def add_article(self, magazine, title):
        from models.article import Article
        new_article = Article(title= title, author_id = self.id, magazine_id= magazine.id)
        db.session.add(new_article)
        db.session.commit()
        return new_article
    
    def topic_areas(self):
        result = db.session.execute(
            """
                SELECT DISTINCT magazines.category FROM magazines
                JOIN articles ON magazines.id = articles.magazine_id
                WHERE articles.author_id = :author_id
            """,
            {"author_id": self.id}
        )
        return [row[0] for row in result.fetchall()]
    
    







