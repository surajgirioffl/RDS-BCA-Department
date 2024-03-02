"""
    @file: orm/admin.py
    @author: Suraj Kumar Giri (@surajgirioffl)
    @init-date: 11th Feb 2024
    @last-modified: 15th Feb 2024
    
    Description:
        * Module containing Models associated with the database 'admin'.
"""

from sqlalchemy import ForeignKey, create_engine, Integer, String, DateTime, Null
from sqlalchemy.orm import mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Roles(Base):
    __tablename__ = "roles"
    id = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    role = mapped_column(String, unique=True, nullable=False)


class Admins(Base):
    __tablename__ = "admins"
    id = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = mapped_column(String, unique=True, nullable=False)
    email = mapped_column(String, unique=True, nullable=False)
    password = mapped_column(String, nullable=False)
    role = mapped_column(String, ForeignKey("roles.role"), nullable=False)
    name = mapped_column(String, nullable=False)
    created_on = mapped_column(DateTime, nullable=False, server_default="CURRENT_TIMESTAMP")


class Permissions(Base):
    __tablename__ = "permissions"
    id = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    permission = mapped_column(String, unique=True, nullable=False)
    super_admin = mapped_column(Integer, nullable=True, default=1)
    admin = mapped_column(Integer, nullable=True, default=None)
    moderator = mapped_column(Integer, nullable=True, default=None)
    user = mapped_column(Integer, nullable=True, default=None)


class ActionsLog(Base):
    __tablename__ = "actions_log"
    sno = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = mapped_column(String, nullable=False)
    action_description = mapped_column(String, nullable=False)
    action_timestamp = mapped_column(DateTime, nullable=False, server_default="CURRENT_TIMESTAMP")


class AdminManager(Base):
    __tablename__ = "admin_manager"
    sno = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = mapped_column(String, unique=True, nullable=False)
    is_allowed = mapped_column(Integer, nullable=True, default=1)


# engine = create_engine("sqlite:///admin.db", echo=True)
engine = create_engine("sqlite:///admin.db")
Base.metadata.create_all(engine)
