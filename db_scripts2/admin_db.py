"""
    @file: db_scripts2/admin_db.py
    @author: Suraj Kumar Giri (@surajgirioffl)
    @init-date: 16th Feb 2024
    @last-modified: 16th Feb 2024
    
    Description:
        * Module to handle database operations related with the database 'admin'.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import admin_model


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


def fetch_granted_permissions(username: str):
    """Fetch granted permission of the given username.

    Args:
        username (str): username to fetch granted permission.

    Returns:
        dict | False: Dictionary of granted permission if user exits and allowed to access admin panel else False.
    """
    engine = create_engine("sqlite:///admin.db")
    session: Session = sessionmaker(engine)()

    if admin_details := fetch_admin_details(username):
        if session.query(admin_model.AdminManager.is_allowed).filter(admin_model.AdminManager.username == username).first():
            permissions = session.query(admin_model.Permissions.permission, getattr(admin_model.Permissions, admin_details["role"])).all()
            permission_dict = {}
            for row in permissions:
                permission_dict[row[0]] = bool(row[1])
            return permission_dict

    return False
