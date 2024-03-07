from model import Base 
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import String,Column,Integer,DateTime
from datetime import datetime,timedelta
class User(Base):

    __tablename__="user"
    id=Column(Integer, primary_key=True, autoincrement=True)
    email=Column(String(100),nullable=False)
    username=Column(String(100),nullable=False)
    password=Column(String(255), nullable=False)
    token=Column(String(255), unique=True ,nullable= True)
    reset_token_expiry=Column(DateTime, nullable=True)
    posts=relationship('Post', backref='users',lazy=True)
   
    def generate_reset_token(self, expiration_hours=1):
        # Generate a reset token using uuid4
        self.token = str(uuid.uuid4())
        self.reset_token_expiry= datetime.utcnow() + timedelta(hours=expiration_hours)

    def is_reset_token_valid(self):
        # Check if the reset token is not expired
        return self.reset_token_expiry is not None and datetime.utcnow() <= self.reset_token_expiration