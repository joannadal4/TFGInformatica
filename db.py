from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_route = "postgresql://postgres:postgres@postgres:5432/modelvpf"
engine = create_engine(db_route, echo = True)

Session = sessionmaker(bind=engine)
