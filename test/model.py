#!/usr/bin/python3
from os import getenv
from datetime import datetime
from sqlalchemy import String,Column,Integer,DateTime
from sqlalchemy.ext.declarative import declarative_base


Base=declarative_base()

class Item(Base):

    __tablename__="form"
    id=Column(Integer, primary_key=True)
    username=Column(String)
    email=Column(String)
    created_at=Column(DateTime,nullable=False,default=datetime.utcnow())
    