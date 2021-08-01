from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_ROUTE


engine = create_engine(DB_ROUTE, echo = True)

Session = sessionmaker(bind=engine)
