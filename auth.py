"""
    @file: auth.py
    @author: Suraj Kumar Giri (@surajgirioffl)
    @init-date: 16th Feb 2024
    @last-modified: 17th Feb 2024
    
    Description:
        Module to handle various authentication methods.
"""

from flask import session


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
