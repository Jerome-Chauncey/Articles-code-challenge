from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
import pytest

def test_article_has_author_magazine_title():
    author = Author("Jerome")
    mag = Magazine("Weekly Code", "Programming")
    article = Article(author, mag, "Best Python Tips")
    
    assert article.author == author
    assert article.magazine == mag
    assert article.title == "Best Python Tips"
