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

    def remove_all_expired_OTPs(self):
        """Removes all expired OTPs from the database.

        Remove all expired OTPs from the 'otp' table and move them into the 'otp_log' table with 'expired' status.
        """
        expired_otp_instances = self.session.query(utilities_model.Otp).filter(utilities_model.Otp.expiration_time < datetime.now()).all()
        for otp_instance in expired_otp_instances:
            otp_log_instance = utilities_model.OtpLog(
                username=otp_instance.username, otp=otp_instance.otp, status="expired", creation_time=otp_instance.creation_time
            )
            self.insert(otp_log_instance)
            self.session.delete(otp_instance)
            self.session.commit()

    def is_valid_otp(self, otp: str, username: str):
        """Check if the provided OTP is valid for the given username.

        This method first remove all expired OTPs from the 'otp' table and move them into the 'otp_log' table with 'expired' status using 'remove_all_expired_OTPs()' method.
        Then it fetch all OTPs from the 'otp' table for the given username.
        And then check if given OTP matches any of the fetched OTPs.
        If the OTP matches, it is considered valid and OTP is deleted from the 'otp' table and moved to 'otp_log' table with 'verified' status and rest OTPs of the same user are moved to 'otp_log' table with 'generated' status.
        If the OTP does not match any of the fetched OTPs, it is considered invalid and no action is taken.
        On match True is returned else False.


        Args:
            otp (str): The OTP to be validated.
            username (str): The username associated with the OTP.

        Returns:
            bool: True if the OTP is valid, False otherwise.
        """
        self.remove_all_expired_OTPs()
        # otp_instances = self.session.query(utilities_model.Otp).filter(utilities_model.Otp.otp == otp, utilities_model.Otp.username == username).all()
        otp_instances = self.session.query(utilities_model.Otp).filter(utilities_model.Otp.username == username).all()
        OTPs = [otp_instance.otp for otp_instance in otp_instances]
        if otp not in OTPs:
            return False  # User may write again. So, we are not going to delete OTPs.

        for otp_instance in otp_instances:
            if otp_instance.otp == otp:
                otp_log_instance = utilities_model.OtpLog(
                    username=otp_instance.username, otp=otp_instance.otp, status="verified", creation_time=otp_instance.creation_time
                )
            else:
                otp_log_instance = utilities_model.OtpLog(
                    username=otp_instance.username, otp=otp_instance.otp, status="generated", creation_time=otp_instance.creation_time
                )
            self.insert(otp_log_instance)
            self.session.delete(otp_instance)
            self.session.commit()

        return True

    def insert_new_otp(self, username: str, otp: str, expires_after: int = 3) -> None:
        """Insert a new OTP for a given username with the specified expiration time.

        Args:
            username (str): The username for which the OTP is being inserted.
            otp (str): The OTP to be inserted.
            expires_after (int, optional): The duration in minutes after which the OTP expires. Defaults to 3.

        Returns:
            None
        """
        if isinstance(otp, int):
            otp = str(otp)
        otp_instance = utilities_model.Otp(
            username=username, otp=otp, creation_time=datetime.now(), expiration_time=datetime.now() + timedelta(minutes=expires_after)
        )
        self.insert(otp_instance)
