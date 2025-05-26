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
    Base.metadata.create_all(engine)  # This creates all tables from your models
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

def test_author_initialization(session):
    # Step 1: Create an Author instance with a 'name' attribute
    author = Author(name="John Doe")
    
    # Step 2: Add author to the session and commit to save to DB
    session.add(author)
    session.commit()
    
    # Step 3: Retrieve the author by name and check attributes
    found = session.query(Author).filter_by(name="John Doe").first()
    assert found is not None, "Implement Author model with 'name' attribute and save to DB"
    assert found.name == "John Doe", "Ensure 'name' is saved and retrieved correctly"

def test_author_name_validation(session):
    # Step 4: Implement validation in Author model to disallow empty names
    # Hint: Raise ValueError in the setter or constructor if name is empty
    with pytest.raises(ValueError):
        author = Author(name="")  # Should raise error
        session.add(author)
        session.commit()

def test_magazine_initialization(session):
    # Step 5: Create Magazine with 'name' and 'category' attributes
    mag = Magazine(name="Tech Today", category="Technology")
    session.add(mag)
    session.commit()
    
    # Step 6: Retrieve magazine by name and category
    found = session.query(Magazine).filter_by(name="Tech Today").first()
    assert found is not None, "Implement Magazine model with 'name' and 'category'"
    assert found.category == "Technology", "Make sure category is saved and retrievable"

def test_magazine_validation(session):
    # Step 7: Add validation for Magazine name and category (no empty strings)
    with pytest.raises(ValueError):
        mag = Magazine(name="", category="Business")
        session.add(mag)
        session.commit()
    with pytest.raises(ValueError):
        mag = Magazine(name="Biz Mag", category="")
        session.add(mag)
        session.commit()

def test_article_initialization_and_relations(session):
    # Step 8: Create Author and Magazine instances first
    author = Author(name="Alice Author")
    mag = Magazine(name="Science Monthly", category="Science")
    session.add_all([author, mag])
    session.commit()
    
    # Step 9: Create Article with 'title' and relationships to Author and Magazine
    article = Article(title="Discovering Space", author=author, magazine=mag)
    session.add(article)
    session.commit()
    
    # Step 10: Retrieve the article and check related author and magazine
    found = session.query(Article).filter_by(title="Discovering Space").first()
    assert found is not None, "Implement Article model with 'title', 'author', 'magazine' relations"
    assert found.author.name == "Alice Author", "Ensure Article.author relationship works"
    assert found.magazine.name == "Science Monthly", "Ensure Article.magazine relationship works"

def test_article_title_validation(session):
    # Step 11: Add validation to disallow empty titles in Article model
    author = Author(name="Bob")
    mag = Magazine(name="Daily News", category="News")
    session.add_all([author, mag])
    session.commit()
    
    with pytest.raises(ValueError):
        article = Article(title="", author=author, magazine=mag)
        session.add(article)
        session.commit()

def test_author_magazine_many_to_many_relationship(session):
    # Step 12: Implement many-to-many relationship between Author and Magazine
    author1 = Author(name="Author One")
    author2 = Author(name="Author Two")
    
    mag1 = Magazine(name="Magazine A", category="Arts")
    mag2 = Magazine(name="Magazine B", category="Business")
    
    # Step 13: Add magazines to authors via many-to-many collection attribute (e.g. author.magazines)
    author1.magazines.append(mag1)
    author1.magazines.append(mag2)
    author2.magazines.append(mag1)
    
    session.add_all([author1, author2, mag1, mag2])
    session.commit()
    
    # Step 14: Verify relationships persisted in both directions
    a1 = session.query(Author).filter_by(name="Author One").first()
    a2 = session.query(Author).filter_by(name="Author Two").first()
    m1 = session.query(Magazine).filter_by(name="Magazine A").first()
    
    assert mag1 in a1.magazines, "author.magazines relationship should contain Magazine A"
    assert mag2 in a1.magazines, "author.magazines relationship should contain Magazine B"
    assert mag1 in a2.magazines, "author.magazines for author2 should contain Magazine A"
    
    assert author1 in m1.authors, "magazine.authors relationship should include Author One"
    assert author2 in m1.authors, "magazine.authors relationship should include Author Two"
