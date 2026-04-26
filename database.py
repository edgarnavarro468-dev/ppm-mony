from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///ppm.db")

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    payer = Column(String)
    amount = Column(Integer)
    description = Column(String)


Base.metadata.create_all(engine)

print("Tablas creadas")