"""
    @file: db_scripts2/admin_db.py
    @author: Suraj Kumar Giri (@surajgirioffl)
    @init-date: 16th Feb 2024
    @last-modified: 25th Feb 2024
    
    Description:
        * Module to handle database operations related with the database 'admin'.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import admin_model
from app_scripts import crypt


class AdminDatabase:
    def __init__(self, engine_url="sqlite:///admin.db") -> None:
        """Constructor for the class initializing the engine URL and session.

        Parameters:
            engine_url (str): The URL of the engine. Defaults to "sqlite:///admin.db".

        Returns:
            None
        """
        self.engine = create_engine(engine_url)
        self.session: Session = sessionmaker(self.engine)()

    def __del__(self) -> None:
        """This function is the destructor method for the class. It commits the current session."""
        self.session.commit()
        self.session.close()

    def check_login_credentials(self, username, password) -> bool:
        """
        Check the login credentials for a given username and password.

        Args:
            username: The username to be checked.
            password: The password to be checked.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """

        # session.query(admin.Admins.password).one()
        if stored_passwords := self.session.query(admin_model.Admins.password).filter(admin_model.Admins.username == username).all():
            password_hash = stored_passwords[0][0]
            return crypt.checkPassword(password, password_hash)
        return False

    def is_admin(self, username: str) -> admin_model.Admins | None:
        """
        Check if the given username is an admin by querying the 'admin' database.

        Args:
            username: The username to be checked.

        Returns:
            admin.Admins | None: The admin object if the username is an admin, None otherwise.
        """
        return self.session.query(admin_model.Admins).filter(admin_model.Admins.username == username).first()

    def fetch_admin_details(self, username) -> dict | bool:
        """
        Fetches the details of the admin with the given username from the admin database.

        Args:
            username (str): The username of the admin.

        Returns:
            dict | bool: Returns a dictionary containing the admin details if the admin is found, otherwise returns False.
        """

        # session.query(admin.Admins.password).one()
        if admin_obj := self.session.query(admin_model.Admins).filter(admin_model.Admins.username == username).first():
            data = {}
            data["username"] = admin_obj.username
            data["email"] = admin_obj.email
            data["role"] = admin_obj.role
            data["name"] = admin_obj.name
            return data
        return False

    def fetch_granted_permissions(self, username: str):
        """Fetch granted permission of the given username.

        Args:
            username (str): username to fetch granted permission.

        Returns:
            dict | False: Dictionary of granted permission if user exits and allowed to access admin panel else False.
        """

        if admin_details := self.fetch_admin_details(username):
            if self.session.query(admin_model.AdminManager.is_allowed).filter(admin_model.AdminManager.username == username).first():
                permissions = self.session.query(
                    admin_model.Permissions.permission, getattr(admin_model.Permissions, admin_details["role"])
                ).all()
                permission_dict = {}
                for row in permissions:
                    permission_dict[row[0]] = bool(row[1])
                return permission_dict

        return False
