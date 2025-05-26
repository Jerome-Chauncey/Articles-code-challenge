from sqlalchemy import Table, Column, Integer, ForeignKey
from lib.models.base import Base

author_magazine = Table(
    "author_magazine", Base.metadata,
    
    Column("author_id", Integer, ForeignKey("authors.id"), primary_key=True),
    Column("magazine_id", Integer, ForeignKey("magazines.id"), primary_key=True)
)
