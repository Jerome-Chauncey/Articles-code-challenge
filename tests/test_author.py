import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

@pytest.fixture
def setup_author_data():
    author = Author("Jerome")
    mag1 = Magazine("Tech Today", "Tech")
    mag2 = Magazine("Food Weekly", "Cuisine")
    article1 = Article(author, mag1, "AI Trends")
    article2 = Article(author, mag2, "Vegan Recipes")
    article3 = Article(author, mag1, "Cybersecurity")
    return author, mag1, mag2, article1, article2, article3

def test_author_has_name(setup_author_data):
    author, *_ = setup_author_data
    assert author.name == "Jerome"

def test_author_articles(setup_author_data):
    author, _, _, article1, _, _ = setup_author_data
    assert len(author.articles()) == 3
    assert article1 in author.articles()

def test_author_magazines(setup_author_data):
    author, mag1, mag2, *_ = setup_author_data
    assert set(author.magazines()) == {mag1, mag2}

def test_author_topic_areas(setup_author_data):
    author, *_ = setup_author_data
    assert "Tech" in author.topic_areas()
    assert "Cuisine" in author.topic_areas()
