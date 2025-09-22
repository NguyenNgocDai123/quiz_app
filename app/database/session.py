from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.core.config import DATABASE_URL

# Tạo engine
engine = create_engine(DATABASE_URL, echo=True)

# Tạo session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class cho models
Base = declarative_base()


# Dependency để lấy session
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
