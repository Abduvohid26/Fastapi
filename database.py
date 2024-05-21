from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(
    'postgresql://postgres:2629@localhost/Delivery_project', echo=True
)

Base = declarative_base()
session = sessionmaker(bind=engine, autoflush=False)
