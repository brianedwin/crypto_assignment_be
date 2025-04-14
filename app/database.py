from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Konfigurasi Database PostgreSQL
DATABASE_URL = "postgresql://user_mybank:mybank123@localhost/mybank"

# Buat engine untuk koneksi ke database
engine = create_engine(DATABASE_URL)

# ORM Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Model untuk SQLAlchemy
Base = declarative_base()

# Dependency untuk mendapatkan session database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

