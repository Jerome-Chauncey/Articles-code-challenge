def test_author_has_name(session):
    from lib.models.author import Author

    author = Author(name="Jerome")
    session.add(author)
    session.commit()

    retrieved_author = session.query(Author).first()
    assert retrieved_author.name == "Jerome"
