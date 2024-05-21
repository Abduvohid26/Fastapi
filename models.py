from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(Text, nullable=False)
    is_active = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    orders = relationship('Orders', back_populates='user')

    def __repr__(self):
        return f'{self.username} {self.email}'
    

class Orders(Base):
    __tablename__ = 'orders'
    ORDER_STATUS = (
        ('PENDING', 'PENDING'),
        ('IN_TRANSIT', 'IN_TRANSIT'),
        ('DELIVERED', 'DELIVERED'),
    )

    id = Column(Integer, primary_key=True)
    qty = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUS), default='PENDING')
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship('Users', back_populates='orders')
    product_id = Column(Integer, ForeignKey('products.id'))
    products = relationship('Product', back_populates='orders')


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
