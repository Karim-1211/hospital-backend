from app.database.db import engine
from app.database.base import Base

# Import ALL models so SQLAlchemy knows about them
from app.models import *

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

if __name__ == "__main__":
    create_tables()