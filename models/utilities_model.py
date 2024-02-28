"""
    @file: orm/utilities_model.py
    @author: Suraj Kumar Giri (@surajgirioffl)
    @init-date: 27th Feb 2024
    @last-modified: 28th Feb 2024
    
    Description:
        * Module containing Models associated with the database 'utilities'.
"""

from datetime import datetime
from sqlalchemy import Integer, String, Enum, DateTime, create_engine
from sqlalchemy.orm import mapped_column, DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


class Otp(Base):
    __tablename__ = "otp"
    id = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = mapped_column(String, nullable=False)
    otp = mapped_column(String, nullable=False)
    creation_time = mapped_column(DateTime, nullable=False, default=datetime.now())
    expiration_time = mapped_column(DateTime, nullable=False)


class OtpLog(Base):
    __tablename__ = "otp_log"
    id = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = mapped_column(String, nullable=False)
    otp = mapped_column(String, nullable=False)
    status = mapped_column(Enum("generated", "verified", "expired"), nullable=False)
    creation_time = mapped_column(DateTime, nullable=False)
    logged_time = mapped_column(DateTime, nullable=False, default=datetime.now())


engine = create_engine("sqlite:///utilities.db")
Base.metadata.create_all(engine)
