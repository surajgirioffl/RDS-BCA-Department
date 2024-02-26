"""
    @file: admin/db_session_manager..py
    @author: Suraj Kumar Giri (@surajgirioffl)
    @init-date: 27th Feb 2024
    @last-modified: 27th Feb 2024
    
    Description:
        * Module to handle db session for the admin panel.
"""

from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def get_sqlite_db_session(database: str) -> Session:
    """Function to get a SQLite database session.

    Args:
        database (str): The name of the database.

    Returns:
        Session: A session object connected to the specified SQLite database.
    """
    engine = create_engine(f"sqlite:///{database}.db")
    return sessionmaker(bind=engine)()
