"""
    @file: auth.py
    @author: Suraj Kumar Giri (@surajgirioffl)
    @init-date: 16th Feb 2024
    @last-modified: 26th Feb 2024
    
    Description:
        Module to handle various authentication methods.
"""

from flask import session
from db_scripts2 import admin_db


def is_admin_logged_in() -> bool:
    """Check if an admin is logged in by verifying the presence of "username" and "admin" in the session.

    Warning - This method will check if admin logged-in using session only. There is no interaction with database.
    It may possible that user is not allowed to access admin panel even if user is set as admin in the session.
    So, Must check database before proceeding to next.

    Returns:
        bool: True if the admin is logged in, otherwise returns False.
    """
    if "username" in session and "admin" in session:
        if session.get("admin"):
            return True
    return False


def authenticate_admin(username: str | None = None) -> tuple[bool, str]:
    """A function to authenticate an admin user, with an optional username parameter.

    Function to authenticate user with 3 steps verification.
        1. Checking if user logged-in via session. (Session must be accessible. So, This function must be called within the request context.)
        2. Checking if username exists in the admin database. If username exists in the admin database, then user will considered as an admin.
        3. Checking if username is allowed to access admin panel. If username is allowed to access admin panel, then only he can access admin panel. (Note: SuperAdmin can restrict any admin to access admin panel.)
    Must use this method authentication for accessing all models.

    Args:
        username (str | None, optional): The username of the admin. Defaults to None. If None then it will be taken from session.

    Returns:
        tuple[bool, str]: Tuple (True, "") if the admin is authenticated and passed 3 steps verification else a tuple (False, str) indicating authentication status(False) and respective message.
    """
    if username is None:
        username = session.get("username")  # returns None if session don't have key 'username'.

    admin_db_instance = admin_db.AdminDatabase()

    # Implementing 3 steps verification of admin.
    # 1. Checking if user logged-in via session
    if is_admin_logged_in():
        # 2. Checking if username exists in the admin database
        if admin_db_instance.is_admin(username):
            # 3. Checking if username is allowed to access admin panel
            if admin_db_instance.is_allowed_to_access_admin_panel(username):
                return True, ""  # Access Granted
            else:
                # User is admin but not allowed to access admin panel.
                return False, "restricted"  # You are restricted to access the admin panel. Contact administrator
        else:
            # User is logged-in but not an admin.
            return False, "denied"  # Access Denied. You are not an admin.

    # User is not logged-in.
    return False, "anonymous"  # Please login to continue.
