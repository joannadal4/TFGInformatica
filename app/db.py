from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DB_ROUTE


engine = create_engine(DB_ROUTE, echo = False)

Session = sessionmaker(bind=engine)
