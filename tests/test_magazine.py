import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

@pytest.fixture
def setup_magazine_data():
    author1 = Author("Jerome")
    author2 = Author("Alex")
    mag = Magazine("Tech Times", "Technology")
    article1 = Article(author1, mag, "AI")
    article2 = Article(author1, mag, "Robotics")
    article3 = Article(author1, mag, "Cybersecurity")
    return author1, author2, mag

def test_magazine_title_and_category(setup_magazine_data):
    _, _, mag = setup_magazine_data
    assert mag.title == "Tech Times"
    assert mag.category == "Technology"

def test_magazine_contributors(setup_magazine_data):
    author1, _, mag = setup_magazine_data
    assert author1 in mag.contributors()

def test_magazine_contributing_authors(setup_magazine_data):
    author1, author2, mag = setup_magazine_data
    assert author1 in mag.contributing_authors()
    assert author2 not in mag.contributing_authors()
