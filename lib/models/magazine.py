from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from lib.models.base import Base

class Magazine(Base):
    __tablename__ = "magazines"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    category = Column(String)

    articles = relationship("Article", back_populates="magazine")