import uuid
from sqlalchemy import Column, String, DateTime, create_engine  
from sqlalchemy.dialects.postgresql import UUID  # Import PostgreSQL native UUID
from sqlalchemy.orm import declarative_base, sessionmaker

# Database Connection 
DATABASE_URL = "postgresql://admin_user:administrator@localhost:5432/misconception_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

     # Explicitly configure SQLAlchemy to use the "auth" schema
    __table_args__ = {"schema": "auth"}

    # Primary key is a UUID. 
    # default=uuid.uuid4 tells SQLAlchemy to create a new unique ID for every new user.
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        unique=True, 
        nullable=False
    )

    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=True)

    # Helper function to create tables automatically 
    # Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()