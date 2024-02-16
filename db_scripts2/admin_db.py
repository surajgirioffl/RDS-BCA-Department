"""
    @file: db_scripts2/admin_db.py
    @author: Suraj Kumar Giri (@surajgirioffl)
    @init-date: 16th Feb 2024
    @last-modified: 16th Feb 2024
    
    Description:
        * Module to handle database operations related with the database 'admin'.
"""

from models import admin_model
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine


def fetch_admin_details(username) -> dict | bool:
    """
    Fetches the details of the admin with the given username from the admin database.

    Args:
        username (str): The username of the admin.

    Returns:
        dict | bool: Returns a dictionary containing the admin details if the admin is found, otherwise returns False.
    """
    engine = create_engine("sqlite:///admin.db")
    session: Session = sessionmaker(engine)()

    # session.query(admin.Admins.password).one()
    if admin_obj := session.query(admin_model.Admins).filter(admin_model.Admins.username == username).first():
        data = {}
        data["username"] = admin_obj.username
        data["email"] = admin_obj.email
        data["role"] = admin_obj.role
        data["name"] = admin_obj.name
        return data
    return False
