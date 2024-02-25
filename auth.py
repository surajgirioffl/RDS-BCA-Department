"""
    @file: auth.py
    @author: Suraj Kumar Giri (@surajgirioffl)
    @init-date: 16th Feb 2024
    @last-modified: 17th Feb 2024
    
    Description:
        Module to handle various authentication methods.
"""

from flask import session
from db_scripts2 import admin_db


def is_admin_logged_in() -> bool:
    """
    Check if an admin is logged in by verifying the presence of "username" and "admin" in the session.

    Returns:
        bool: True if the admin is logged in, otherwise returns False.
    """
    if "username" in session and "admin" in session:
        if session.get("admin"):
            return bool(admin_db.AdminDatabase().is_admin(session.get("username")))
    return False
