"""
    @file: orm/dynamic_contents.py
    @author: Suraj Kumar Giri (@surajgirioffl)
    @init-date: 11th Feb 2024
    @last-modified: 15th Feb 2024
    
    Description:
        * Module containing Models associated with the database 'dynamic_contents'.
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Notice(Base):
    __tablename__ = "notice"
    SNo = Column(Integer, primary_key=True, autoincrement=True)
    TopMarquee = Column(String(300), nullable=False)
    TopMarqueeLink = Column(String(100), default=None)
    Title = Column(String(300), nullable=False)
    DocsDownloadTitle = Column(String(200), nullable=False)
    DocsDownloadLink = Column(String(100), default=None)
    ButtonTitle = Column(String(200), default=None)
    ButtonLink = Column(String(100), default=None)
    BlinkerTitle = Column(String(80), nullable=False)
    BlinkingText = Column(String(50), nullable=False)
    BottomMarquee1 = Column(String(300), nullable=False)
    BottomMarquee2 = Column(String(300), default=None)
    BottomMarquee3 = Column(String(300), default=None)
    DateModified = Column(DateTime, nullable=False, server_default="CURRENT_TIMESTAMP")


class Credits(Base):
    __tablename__ = "credits"
    SNo = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False)
    Designation = Column(String(50), default=None)
    Contributions = Column(String(200), nullable=False)
    ContactTitle = Column(String(50), default=None)
    ContactLink = Column(String(100), default=None)


class Sources(Base):
    __tablename__ = "sources"
    SNo = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False)
    Contributions = Column(String(200), nullable=False)
    Link = Column(String(100), default=None)


class Teachers(Base):
    __tablename__ = "teachers"
    SNo = Column(Integer, unique=True, nullable=False, autoincrement=True)
    TeacherId = Column(Integer, primary_key=True, nullable=False)
    Name = Column(String(50), nullable=False)
    Qualifications = Column(String(100), default=None)
    Subjects = Column(String(300), nullable=False)
    PhoneNo = Column(String(15), unique=True, default=None)
    Email = Column(String(100), unique=True, default=None)
    SocialLink = Column(String(100), unique=True, default=None)


# engine = create_engine("mysql://username:password@localhost/dynamic_contents")
# Base.metadata.create_all(engine)
