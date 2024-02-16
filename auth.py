"""
    @file: auth.py
    @author: Suraj Kumar Giri (@surajgirioffl)
    @init-date: 16th Feb 2024
    @last-modified: 16th Feb 2024
    
    Description:
        Module to handle various authentication methods.
"""

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from orm import admin_model as admin
from app_scripts import crypt


def check_login_credentials(username, password) -> bool:
    """
    Check the login credentials for a given username and password.

    Args:
        username: The username to be checked.
        password: The password to be checked.

    Returns:
        bool: True if the credentials are valid, False otherwise.
    """
    engine = create_engine("sqlite:///admin.db")
    session: Session = sessionmaker(engine)()

    # session.query(admin.Admins.password).one()
    if stored_passwords := session.query(admin.Admins.password).filter(admin.Admins.username == username).all():
        password_hash = stored_passwords[0][0]
        return crypt.checkPassword(password, password_hash)
    return False


def is_admin(username: str) -> admin.Admins | None:
    """
    Check if the given username is an admin by querying the 'admin' database.

    Args:
        username: The username to be checked.

    Returns:
        admin.Admins | None: The admin object if the username is an admin, None otherwise.
    """
    engine = create_engine("sqlite:///admin.db")
    session: Session = sessionmaker(engine)()
    # Implement OOPs later to avoid reparations of code.
    return session.query(admin.Admins).filter(admin.Admins.username == username).first()