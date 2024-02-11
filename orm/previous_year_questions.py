"""
    @file: orm/previous_year_questions.py
    @author: Suraj Kumar Giri (@surajgirioffl)
    @init-date: 11th Feb 2024
    @last-modified: 11th Feb 2024
    
    Description:
        * Module containing Models associated with the database 'previous_year_questions'.
"""

from sqlalchemy import create_engine, Column, Integer, SmallInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Brabu(Base):
    __tablename__ = "brabu"
    SNo = Column(Integer, nullable=False, unique=True, autoincrement=True)
    Year = Column(SmallInteger, primary_key=True, nullable=False)
    Sem1 = Column(Integer, unique=True, default=None)
    Sem2 = Column(Integer, unique=True, default=None)
    Sem3 = Column(Integer, unique=True, default=None)
    Sem4 = Column(Integer, unique=True, default=None)
    Sem5 = Column(Integer, unique=True, default=None)


class LnMishra(Base):
    __tablename__ = "ln_mishra"
    SNo = Column(Integer, nullable=False, unique=True, autoincrement=True)
    Year = Column(SmallInteger, primary_key=True, nullable=False)
    Sem1 = Column(Integer, unique=True, default=None)
    Sem2 = Column(Integer, unique=True, default=None)
    Sem3 = Column(Integer, unique=True, default=None)
    Sem4 = Column(Integer, unique=True, default=None)
    Sem5 = Column(Integer, unique=True, default=None)


class Vaishali(Base):
    __tablename__ = "vaishali"
    SNo = Column(Integer, nullable=False, unique=True, autoincrement=True)
    Year = Column(SmallInteger, primary_key=True, nullable=False)
    Sem1 = Column(Integer, unique=True, default=None)
    Sem2 = Column(Integer, unique=True, default=None)
    Sem3 = Column(Integer, unique=True, default=None)
    Sem4 = Column(Integer, unique=True, default=None)
    Sem5 = Column(Integer, unique=True, default=None)


# engine = create_engine("mysql://username:password@localhost/previous_year_questions")
# Base.metadata.create_all(engine)
