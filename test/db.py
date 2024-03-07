
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine=create_engine("mysql+mysqldb://david:password@localhost/school",pool_pre_ping=True)


Session=sessionmaker(bind=engine)
session=Session()


