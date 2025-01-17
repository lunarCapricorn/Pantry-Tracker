from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///pantry.db')
Base = declarative_base()


class Product(Base):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key=True)
    name = Column('Product_Name', String)
    how_much_left = Column('How_Much_Left, grams', Float)
    cost = Column('Cost, euro', Float)

    def __init__(self, name, how_much_left, cost):
        self.name = name
        self.how_much_left = how_much_left
        self.cost = cost

    def __repr__(self):
        return f'{self.name}, {self.how_much_left}g, {self.cost}eu'

Base.metadata.create_all(engine)