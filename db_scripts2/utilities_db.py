"""
    @file: db_scripts2/utilities_db.py
    @author: Suraj Kumar Giri (@surajgirioffl)
    @init-date: 27th Feb 2024
    @last-modified: 27th Feb 2024
    
    Description:
        * Module to handle database operations related with the database 'utilities'.
"""

from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import utilities_model


class UtilitiesDB:
    def __init__(self, engine_url="sqlite:///utilities.db") -> None:
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

    def insert(self, model_instance) -> None:
        """Inserts a model instance (row) into the session and commits the changes.

        Args:
            model_instance: The model instance to be inserted.

        Returns:
            None
        """
        self.session.add(model_instance)
        self.session.commit()
