from .base import Base
from .author import Author
from .article import Article
from .magazine import Magazine

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()