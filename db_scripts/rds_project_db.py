"""
    @description: Module to handle all database related operation for the API of  the project 'rds-college'.
    @error-series: 2100
    @init-date: 9th April 2023
    @last-updated: 9th April 2023
"""
from automation_scripts import my_random as myRandom
from os import environ
import os
import sys
import mysql.connector as mysql
# to import the module 'myRandom' from the parent directory
sys.path.append(os.getcwd())


class RdsProject:
    """
        Description:
            - Class to handle all database related operation for the API of  the project 'rds-college'.
            - Made for Gaurav Srivasatava and Saurabh Anand's project.
    """

    def __init__(self, host: str = environ.get('DBHOST'), user: str = environ.get('DBUSERNAME'), port: int = int(environ.get('DBPORT')) if environ.get('DBPORT') is not None else 3306, password: str = environ.get('DBPASSWORD'), database: str = 'rds_project') -> None:
        """
            Description:
                - Constructor for the class RdsProject.
                - This method will create a connection to the database and will create a cursor.
            Parameters:
                - host: The host of the database.
                - user: The username of the database.
                - port: The port of the database.
                - password: The password of the database.
            Returns:
                - None
        """
        try:
            self.conn = mysql.connect(
                host=host, user=user, port=port, password=password)
            self.cursor = self.conn.cursor(buffered=True)

            database = f"rdsbca${database}"
            self.cursor.execute(f"""-- sql
                                    USE `{database}`
                                """)
            self.connectionStatus = True  # flag to check if connection is established or not
            print(f"Connection established with the database {database}.")
        except Exception as e:
            print(
                f"Unable to connect with the database {database}. Error code 2100")
            print("Exception:", e)
            self.connectionStatus = False  # if connection not established

    def __del__(self):
        """
            Description:
                - To close the database connection when destructor called.
        """
        if self.connectionStatus:
            self.conn.commit()
            self.conn.close()

    def saveStudentDetails(self, studentsData: dict) -> bool:
        studentsData['id'] = myRandom.Random(
            self.cursor, tableName='students', columnName='id').generate()
        try:
            self.cursor.execute(f"""-- sql
                                    INSERT INTO students(id, email, password, first_name, gender)
                                    VALUES
                                    ({studentsData.get('id')}, '{studentsData.get('email')}', '{studentsData.get('password')}',
                                    '{studentsData.get('firstname')}', '{studentsData.get('gender')}')
                                """)
            self.cursor.execute(f"""-- sql
                                    INSERT INTO students_details(id, middle_name, last_name, course, country_code, phone_number, address)
                                    VALUES
                                    ({studentsData.get('id')}, '{studentsData.get('middlename')}', '{studentsData.get('lastname')}',
                                    '{studentsData.get('course')}', '{studentsData.get('country_code')}', '{studentsData.get('phone')}',
                                    '{studentsData.get('address')}')
                                """)
        except Exception as e:
            print(
                "Something went wrong while saving data into the database. Error code 2101")
            print("Exception:", e)
            return False
        else:
            print("Data about students saved successfully into the database.")
            return True

    def saveContactFormDetails(self, contactFormData: dict) -> bool:
        try:
            self.cursor.execute(f"""-- sql
                                    INSERT INTO contact(sno, email, first_name, last_name, country, contents)
                                    VALUES
                                    (DEFAULT, '{contactFormData.get('email')}', '{contactFormData.get('firstname')}',
                                    '{contactFormData.get('lastname')}', '{contactFormData.get('country')}', "{contactFormData.get('contents')}")
                                """)
        except Exception as e:
            print(
                "Something went wrong while saving data into the database. Error code 2102")
            print("Exception:", e)
            return False
        else:
            print("Data from the contact form saved successfully into the database.")
            return True

    def fetchAllStudentDetails(self) -> list:
        try:
            self.cursor.execute("""-- sql
                                    SELECT students.id, first_name, email, course
                                    FROM 
                                    students INNER JOIN students_details
                                    ON students.id = students_details.id
                                """)
        except Exception as e:
            print(
                "Something went wrong while fetching all data of students from the database. Error code 2103")
            print("Exception:", e)
        else:
            return self.cursor.fetchall()

    def fetchStudentDetails(self, studentID: int) -> list:
        try:
            self.cursor.execute(f"""-- sql
                                    SELECT students.id, first_name, middle_name, last_name, gender, email, course, country_code, phone_number, address
                                    FROM 
                                    students INNER JOIN students_details
                                    ON students.id = students_details.id 
                                    WHERE students.id = {studentID}
                                """)
        except Exception as e:
            print(
                f"Something went wrong while fetching student with id {studentID} from the database. Error code 2104")
            print("Exception:", e)
        else:
            return self.cursor.fetchone()

    def fetchAllContactFormDetails(self):
        try:
            self.cursor.execute(f"""-- sql
                                    SELECT sno, email, first_name, last_name, country
                                    FROM 
                                    contact
                                """)
        except Exception as e:
            print(
                f"Something went wrong while fetching all contact form details from the database. Error code 2105")
            print("Exception:", e)
        else:
            return self.cursor.fetchall()

    def fetchContactFormDetails(self, contactSNo):
        try:
            self.cursor.execute(f"""-- sql
                                    SELECT sno, email, first_name, last_name, country, contents
                                    FROM 
                                    contact
                                    WHERE sno = {contactSNo}
                                """)
        except Exception as e:
            print(
                f"Something went wrong while fetching contact with sno {contactSNo} from the database. Error code 2106")
            print("Exception:", e)
        else:
            return self.cursor.fetchone()

    def deleteStudent(self, studentID: int) -> bool:
        try:
            self.cursor.execute(f"""-- sql
                                    DELETE FROM students
                                    WHERE id = {studentID}
                                """)
            self.cursor.execute(f"""-- sql
                                    DELETE FROM students_details
                                    WHERE id = {studentID}
                                """)
        except Exception as e:
            print(
                f"Something went wrong while deleting student with id {studentID} from the database. Error code 2107")
            print("Exception:", e)
            return False
        else:
            print(
                f"Student with id {studentID} deleted successfully from the database.")
            return True
    
    def deleteContact(self, contactSNo: int) -> bool:
        try:
            self.cursor.execute(f"""-- sql
                                    DELETE FROM contact
                                    WHERE sno = {contactSNo}
                                """)
        except Exception as e:
            print(
                f"Something went wrong while deleting contact with sno {contactSNo} from the database. Error code 2108")
            print("Exception:", e)
            return False
        else:
            print(
                f"Contact with sno {contactSNo} deleted successfully from the database.")
            return True


if __name__ == '__main__':
    print(RdsProject().fetchContactFormDetails(1))
