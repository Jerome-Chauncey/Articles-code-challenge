from models import Author, Article
from lib.models import db

def add_author_with_articles(author_name, articles_data):
    try:
        with db.session.begin():
            author = Author(name=author_name)
            db.session.add(author)
            db.session.flush()

            for article in articles_data:
                new_article = Article(
                    title = article["title"],
                    author_id = author.id,
                    magazine_id = article["magazine_id"]
                )
                db.session.add(new_article)

        return True
    except Exception as e:
        db.session.rollback()
        print(f"Transaction failed: {e}")
        return False
    

