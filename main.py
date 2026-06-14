from app.database.db import engine
from app.database.base import Base
from app.models.user import User

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

if __name__ == "__main__":
    create_tables()