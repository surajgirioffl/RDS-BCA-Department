"""
    @file: mail.py
    @author: Suraj Kumar Giri (@surajgirioffl)
    @init-date: 8th March 2022
    @last-modified: 10th March 2022
    @error-series: 1700
    
    @description:
        Script to send mail (in single or in batch).
    
    @classes:
        * Mail:
            - Class to perform all operations related to mail. 
"""

__author__ = 'Suraj Kumar Giri'
__email__ = 'surajgirioffl@gmail.com'


from flask_mail import Mail as FlaskMail, Message


class Mail:
    """
        Description:
            - Class to perform all operations related to mail.

        Methods:
            * configureApp (static):
                - Method to configure the Flask app for Flask-Mail.
    """
    @staticmethod
    def configureApp(app, **config) -> None:
        """
            Description:
                - Method to configure the Flask app for Flask-Mail.

            Args:
                * app (Flask):
                    - object of class Flask of Flask.
                * config (dict):
                    - Configuration for Flask-Mail.
                    - Keys: MAIL_USERNAME, MAIL_PASSWORD, MAIL_SERVER, MAIL_PORT, MAIL_USE_SSL, MAIL_DEFAULT_SENDER etc...
        """
        app.config['MAIL_USERNAME'] = config['MAIL_USERNAME']
        app.config['MAIL_PASSWORD'] = config['MAIL_PASSWORD']
        app.config['MAIL_SERVER'] = config['MAIL_SERVER']
        try:
            app.config['MAIL_PORT'] = int(config['MAIL_PORT'])
        except Exception as e:
            print("Error in converting MAIL_PORT to int. Error Code: 1701")
            print("Exception: ", e)
            app.config['MAIL_PORT'] = 465
        app.config['MAIL_USE_SSL'] = config['MAIL_USE_SSL']
        app.config['MAIL_DEFAULT_SENDER'] = config['MAIL_DEFAULT_SENDER']

    def __init__(self, app) -> None:
        """
            Description:
                - Constructor of the class Mail.
                - Initializes the Flask-Mail object and configures it for mail services.

            Args:
                * app (Flak): 
                    - object of class Flask of Flask.

        """
        self.mail = FlaskMail(app)

    def sendMessage(self, subject: str, message: str,  recipients: list, html: str, sender: str | None = None) -> bool:
        try:
            msg = Message(subject=subject, body=message,
                        recipients=recipients, sender=sender, html=html)
            self.mail.send(msg)
        except Exception as e:
            print("Unable to send mail. Error Code: 1700")
            print("Exception: ", e)
            return False
        else:
            return True
