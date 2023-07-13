from datetime import datetime
from sqlalchemy import String,Column,Integer,DateTime
from model import Base


class Product(Base):

    __tablename__="tent"
    id=Column(Integer, primary_key=True)
    title=Column(String)
    
