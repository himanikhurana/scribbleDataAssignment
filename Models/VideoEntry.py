from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date


metadata = declarative_base()

class Areas(str, Enum):
    US = "US"
    IN = "IN"
    CA = "CA"
    FR = "FR"
    DE = "DE"

class VideoEntry(BaseModel):
    video_id: str
    trending_date: date
    title: str
    channel_title: str
    group_id: int
    tags: str
    area: str
    views: int
    likes: int
    dislikes: int
    comment_count: int
    group_title: str
    description: str

class VideoEntryDB(metadata):
    __tablename__ = "video_entries"

    video_id = Column(String, primary_key=True, index=True)
    trending_date = Column(Date, primary_key=True, index=True)
    title = Column(String)
    channel_title = Column(String)
    group_id = Column(Integer)
    tags = Column(String)
    area = Column(String, primary_key=True, index=True)
    views = Column(Integer)
    likes = Column(Integer)
    dislikes = Column(Integer)
    comment_count = Column(Integer)
    group_title = Column(String)
    description = Column(String)
    
