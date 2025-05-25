import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.models.base import Base
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

@pytest.fixture(scope="module")
def test_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture(scope="function")
def session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

def test_create_author(session):
    author = Author(name="John Doe")
    session.add(author)
    session.commit()

    retrieved = session.query(Author).filter_by(name="John Doe").first()
    assert retrieved is not None
    assert retrieved.name == "John Doe"

def test_create_magazine(session):
    magazine = Magazine(name="Tech Today", category="Technology")
    session.add(magazine)
    session.commit()

    retrieved = session.query(Magazine).filter_by(name="Tech Today").first()
    assert retrieved is not None
    assert retrieved.name == "Tech Today"
    assert retrieved.category == "Technology"

def test_create_article(session):
    author = Author(name="Alice Author")
    magazine = Magazine(name="Science Monthly", category="Science")
    session.add_all([author, magazine])
    session.commit()

    article = Article(title="Discovering Space", author=author, magazine=magazine)
    session.add(article)
    session.commit()

    retrieved = session.query(Article).filter_by(title="Discovering Space").first()
    assert retrieved is not None
    assert retrieved.title == "Discovering Space"
    assert retrieved.author.name == "Alice Author"
    assert retrieved.magazine.name == "Science Monthly"

def test_author_magazine_many_to_many(session):
    author1 = Author(name="Author One")
    author2 = Author(name="Author Two")

    magazine1 = Magazine(name="Magazine A", category="Arts")
    magazine2 = Magazine(name="Magazine B", category="Business")

    # associate authors and magazines many-to-many
    author1.magazines.append(magazine1)
    author1.magazines.append(magazine2)

    author2.magazines.append(magazine1)

    session.add_all([author1, author2, magazine1, magazine2])
    session.commit()

    # Reload to test
    a1 = session.query(Author).filter_by(name="Author One").first()
    a2 = session.query(Author).filter_by(name="Author Two").first()

    assert len(a1.magazines) == 2
    assert magazine1 in a1.magazines
    assert magazine2 in a1.magazines

    assert len(a2.magazines) == 1
    assert magazine1 in a2.magazines

    m1 = session.query(Magazine).filter_by(name="Magazine A").first()
    assert len(m1.authors) == 2
    assert author1 in m1.authors
    assert author2 in m1.authors

