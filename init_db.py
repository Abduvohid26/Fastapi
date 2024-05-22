from database import Base, engine
from models import User, Product, Order

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")