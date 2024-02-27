"""
    @file: admin/views.py
    @author: Suraj Kumar Giri (@surajgirioffl)
    @init-date: 25th Feb 2024
    @last-modified: 27th Feb 2024
    
    Description:
        * Main module to handle views of admin panel.
"""

from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, flash, url_for, session
import auth
from db_scripts2 import admin_db


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


class __MyBaseModelView(ModelView):
    """Base model view class.

    Base model view class providing functionalities of model specific column to display (pk & fk too) and form column to create (except autoincrement columns).
    It also check if user has access to admin panel and provide appropriate response if not.
    """

    can_view_details = True
    column_display_pk = True

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.model = args[0]

    def is_accessible(self) -> bool:
        is_allowed_to_access, message = auth.authenticate_admin()

        if is_allowed_to_access:
            return True

        self.inaccessible_message = message
        return False

    def inaccessible_callback(self, name, **kwargs):
        # return redirect(url_for("login", next=request.url))
        return get_message_specific_response(self.inaccessible_message)

    @property
    def column_list(self):
        column_list = [column.name for column in self.model.__table__.columns]
        return column_list

    @property
    def form_columns(self):
        form_column_list = self.column_list
        form_columns_to_exclude = ["sno", "id"]  # Like auto-increment, default-valued etc

        for column in form_columns_to_exclude:
            try:
                form_column_list.remove(column)
            except Exception as e:
                continue  # May be in current module, current attribute doesn't exit.

        return form_column_list


class RoleDependentModelView(__MyBaseModelView):
    """
    It will automatic fetch the user role and set the permission as per role to the model view.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def set_attributes(self):
        granted_permissions: dict = admin_db.AdminDatabase().fetch_granted_permissions(session.get("username"))
        for permission, is_allowed in granted_permissions.items():
            setattr(self, permission, is_allowed)

    def is_accessible(self) -> bool:
        is_allowed_to_access, message = auth.authenticate_admin()

        if is_allowed_to_access:
            self.set_attributes()  # Performing an extra operation
            return True

        self.inaccessible_message = message


class ReadOnlyModelView(__MyBaseModelView):
    """
    It will set the model read only irrespective of the user's role.
    """

    can_create = False
    can_edit = False
    can_delete = False


class ModeratorModelView(ModelView): ...


class AdminModelView(ModelView): ...


class SuperAdminModelView(__MyBaseModelView):
    """
    Model view created using this ModeViewClass will accessible to super admin only.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def is_accessible(self) -> bool:
        is_allowed_to_access, message = auth.authenticate_admin()

        if is_allowed_to_access:
            # Means user is an admin and allowed to access admin panel.
            # Let us check if he is super admin.
            admin_data_dict = admin_db.AdminDatabase().fetch_admin_details(session.get("username"))
            if admin_data_dict.get("role") == "super_admin":
                return True
            message = "Access Denied. You are not allowed to access super admin dashboard."

        self.inaccessible_message = message
        return False
