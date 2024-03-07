from model import Base 
from datetime import datetime
from sqlalchemy import DateTime, String,Column,Integer,ForeignKey,Text
class Post(Base):

    __tablename__="post"
    id=Column(Integer, primary_key=True, autoincrement=True)
    date_posted=Column(DateTime,default=datetime.utcnow)
    topic=Column(String(100),nullable=False)
    mentor=Column(String(100),nullable=False)
    date_str=Column(String(10),nullable=False)
    time_str=Column(String(100),nullable=False)
    description=Column(Text,nullable=False)
    duration_str=Column(String(8),nullable=False)  
    user_id=Column(Integer,ForeignKey('user.id'),nullable=False)
