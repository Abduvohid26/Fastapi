from database import Base, engine
from models import User, Product, Orders

Base.metadata.create_all(bind=engine)