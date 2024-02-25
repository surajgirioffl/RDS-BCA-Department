"""
    @file: admin/admin.py
    @author: Suraj Kumar Giri (@surajgirioffl)
    @init-date: 11th Feb 2024
    @last-modified: 25th Feb 2024
    
    Description:
        * Main module to handle admin panel.
"""

from flask import Flask
from flask_admin import Admin
from admin import views


def admin_panel(app: Flask) -> None:
    """Driver function to handle admin panel.

    Args:
        app (Flask): Flask app.
    """
    app.config["FLASK_ADMIN_SWATCH"] = "cerulean"  # Setting bootswatch theme
    admin = Admin(app, name="AdminPanel", template_mode="bootstrap4", index_view=views.MyIndexView())

    # administrative views
    # ....
