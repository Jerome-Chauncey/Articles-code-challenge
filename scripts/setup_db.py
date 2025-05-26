import sys
import os

# 👇 This makes sure Python can find the lib/ folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.db.connection import engine
from lib.models.base import Base

def setup_database():
    
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    setup_database()

    
    



