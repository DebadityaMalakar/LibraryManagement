from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    _id = Column(String(16), primary_key=True, index=True)
    email = Column(String, unique=True)
    name = Column(String)
    password = Column(String)
    salt = Column(String)
    username = Column(String, unique=True, index=True)

class Book(Base):
    __tablename__ = "books"

    _id = Column(Integer, primary_key=True, index=True)
    author = Column(String)
    bought_on = Column(Date)
    due_date = Column(Date)
    end = Column(Date)
    lent_on = Column(Date)
    lentid = Column(String, ForeignKey('users.username'))
    name = Column(String)
    overdue = Column(Integer)  # price in INR for overdue
    price = Column(Float)
    published_on = Column(Date)
    rent = Column(Float)
    start = Column(Date)

    user = relationship("User", back_populates="books")

User.books = relationship("Book", back_populates="user")

# Create the tables
Base.metadata.create_all(bind=engine)
