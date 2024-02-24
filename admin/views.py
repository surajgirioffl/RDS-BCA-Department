"""
    @file: admin/views.py
    @author: Suraj Kumar Giri (@surajgirioffl)
    @init-date: 25th Feb 2024
    @last-modified: 25th Feb 2024
    
    Description:
        * Main module to handle views of admin panel.
"""

from flask_admin import AdminIndexView, expose
from flask import session, redirect, url_for, flash
import auth


class MyIndexView(AdminIndexView):
    """Custom admin panel index view class."""

    @expose("/")
    def index(self):
        if "username" in session:
            if auth.is_admin(session.get("username")):
                # return self.render(self._template)
                return self.render("admin/index.html")
            else:
                # If user is logged-in but not an admin.
                flash("You are not allowed to access the admin panel.", "warning")
                return redirect(url_for("message"))
        else:
            flash("You are not logged-in. Please log-in to access admin panel.")
            return redirect(url_for("login"))
