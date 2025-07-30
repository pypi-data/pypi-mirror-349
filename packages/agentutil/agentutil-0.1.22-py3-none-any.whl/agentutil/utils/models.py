from pydantic import BaseModel, model_validator
from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SAEnum
from sqlalchemy.ext.declarative import declarative_base

class NewsStatus(str, Enum):
    PUBLISHED = "published"
    NEW = "new"
    FAILED = "failed"


Base = declarative_base()

class NewsORM(Base):
    __tablename__ = "news"

    id = Column(String, primary_key=True, autoincrement=True)
    title = Column(String)
    status = Column(String)
    cost = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)  # store duration in seconds

class News(BaseModel):
    title: str
    summary: str = ""
    content: str = ""
    status: NewsStatus = NewsStatus.NEW

    @model_validator(mode='before')
    @classmethod
    def remove_non_bmp(cls, values):
        for field in ['title', 'summary', 'content']:
            if field in values:
                values[field] = ''.join(
                    c for c in values[field] if ord(c) <= 0xFFFF
                )
        return values

