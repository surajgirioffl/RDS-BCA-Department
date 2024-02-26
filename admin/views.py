"""
    @file: admin/views.py
    @author: Suraj Kumar Giri (@surajgirioffl)
    @init-date: 25th Feb 2024
    @last-modified: 26th Feb 2024
    
    Description:
        * Main module to handle views of admin panel.
"""

from flask_admin import AdminIndexView, expose
from flask import redirect, url_for, flash
import auth


def get_message_specific_response(message: str):
    """A function to handle different types of messages and provide specific responses based on the message type.

    Args:
        message(str): A string representing the type of message.

    Returns:
        A redirection based on the message type.
    """
    if message == "restricted":
        # User is admin but not allowed to access admin panel.
        flash("Access Denied. You are not allowed to access the admin panel.", "warning")
        flash("Hi Admin, You are restricted to access the admin panel. Please contact administrator.", "warning")
        return redirect(url_for("message"))
    elif message == "denied":
        # User is logged-in but not an admin.
        flash("Access Denied. You are not allowed to access the admin panel.", "warning")
        return redirect(url_for("message"))
    elif message == "anonymous":
        # User is not logged-in.
        flash("You are not logged-in. Please log-in to access the admin panel.")
        return redirect(url_for("login"))
    else:
        # Something else.
        flash("Access Denied.", "warning")
        return redirect(url_for("message"))


class MyIndexView(AdminIndexView):
    """Custom admin panel index view class."""

    @expose("/")
    def index(self):
        # Authenticating the user.
        is_allowed_to_access, message = auth.authenticate_admin()

        if is_allowed_to_access:
            # Access granted and allowed to access the admin panel.
            # return self.render(self._template)
            return self.render("admin/index.html")

        # Access denied.
        return get_message_specific_response(message)
