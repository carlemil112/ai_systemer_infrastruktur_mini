from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime


DATABASE_URL = "sqlite:///./mydatabase.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, index=True)
    endpoint = Column(String, index=True)     # "classify-image" / "classify-review"
    input_text = Column(String, nullable=True)
    input_image_hash = Column(String, nullable=True)  # fx hash af base64-string
    predicted_label = Column(String)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


    def init_db():
        Base.metadata.create_all(bind=engine)