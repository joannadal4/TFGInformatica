from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_route = "postgresql://postgres:postgres@5432/postgres"
engine = create_engine(db_route, echo = True)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
