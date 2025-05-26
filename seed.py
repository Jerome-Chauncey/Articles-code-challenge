from faker import Faker
from lib.models.base import Base
from lib.db.connection import engine, SessionLocal
from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine
from random import randint, sample, choice

fake = Faker()
session = SessionLocal()

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

authors = [Author(name= fake.name()) for _ in range(5)]
session.add_all(authors)

magazines = [Magazine(name= fake.company(), category = fake.bs().split()[0].capitalize()) for _ in range(5)]
session.add_all(magazines)

session.commit()

for author in authors:
    mags = sample(magazines, k= randint(1,3))
    for mag in mags:
        mag.authors.append(author)

articles = []
for _ in range(10):
    article = Article(
        title = fake.sentence(nb_words=4),
        content = fake.paragraph(nb_sentences=5),
        author = choice(authors),
        magazine = choice(magazines)
    )
    articles.append(article)

session.add_all(articles)
session.commit()