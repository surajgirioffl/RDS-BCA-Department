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
from admin import db_session_manager
from models import admin_model, dynamic_contents, files, previous_year_questions


def admin_panel(app: Flask) -> None:
    """Driver function to handle admin panel.

    Args:
        app (Flask): Flask app.
    """
    app.config["FLASK_ADMIN_SWATCH"] = "cerulean"  # Setting bootswatch theme
    admin = Admin(app, name="AdminPanel", template_mode="bootstrap4", index_view=views.MyIndexView())

    # In below category_models_mapping dict:
    # => role_dependent - Models in this category will be accessible to all roles but permission depends on the role.
    # => read_only - Models in this category will be accessible to all roles but they will read only (no one can create or edit).
    # => super_admin_only - Models in this category will be accessible to super admin only (Permission can be taken from database, BTW not required because only one role permissions can be hardcoded.)
    # Below are not added yet.
    # => admin_only - Models in this category will be accessible to admin and super admin only (Permission will be taken from database as per role after verify if user is admin or super admin)
    # => moderator_only - Models in this category will be accessible to moderator, admin and super admin only. (Permission will be taken from database as per role after verify if user is moderator, admin or super admin)

    category_models_mapping: dict = {
        "role_dependent": {
            "dynamic_contents": [
                dynamic_contents.Notice,
                dynamic_contents.Credits,
                dynamic_contents.Sources,
                dynamic_contents.Teachers,
            ],
            "files": [
                files.Files,
                files.FilesPath,
                files.Drive,
                files.FileContentsInfo,
                files.FilesType,
                files.FilesMetadata,
                files.FilesInfo,
                files.CreditorsInfo,
                files.RootSources,
                files.Credits,
            ],
            "previous_year_questions": [
                previous_year_questions.Brabu,
                previous_year_questions.LnMishra,
                previous_year_questions.Vaishali,
            ],
        },
        "read_only": {
            "files": [
                files.FilesTracking,
                files.FilesViewsTracking,
            ],
        },
        "super_admin_only": {
            "admin": [
                admin_model.Roles,
                admin_model.Admins,
                admin_model.Permissions,
                admin_model.AdminManager,
                admin_model.ActionsLog,
            ],
        },
    }

    category_view_class_mapping = {
        "role_dependent": views.RoleDependentModelView,
        "read_only": views.ReadOnlyModelView,
        "super_admin_only": views.SuperAdminModelView,
    }

    # administrative views
    for category, database_models_dict in category_models_mapping.items():
        for database_name, model_list in database_models_dict:
            # I have used two types of database (sqlite as well as mysql)
            if database_name in ["admin"]:
                db_session = db_session_manager.get_sqlite_db_session(database_name)
            else:
                db_session = db_session_manager.get_mysql_db_session(database_name)

            for model in model_list:
                admin.add_view(category_view_class_mapping[category](model, db_session, category=database_name))
