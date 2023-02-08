"""
    @author: Suraj Kumar Giri
    @init-date: 17th Oct 2022
    @last-modified: 9th Feb 2023
    @error-series: 1400
    @description:
        * Module to handle database operations related to fetching result.
    @classes:
        * Result:
            - Class to handle database operations for student's result.
            - To fetch result of students using various methods.
"""

__author__ = 'Suraj Kumar Giri'
__email__ = 'surajgirioffl@gmail.com'

from os import environ
import mysql.connector as mysql


class Result:
    """
        @description:
            - Class to handle database operations for student's result.

        @methods:
            * getResult():
                - To fetch result of students using various methods (using registrationNo, examRoll, classRoll).
    """

    def __init__(self, session: str, semester: int | str, host: str = environ.get('DBHOST'), user: str = environ.get('DBUSERNAME'), port: int = int(environ.get('DBPORT')) if environ.get('DBPORT') is not None else 3306, password: str = environ.get('DBPASSWORD')) -> None:
        """
            Description:
                - To initialize the database connection and cursor using student's session and semester.

            Args:
                * session (str):
                    - Student's session. E.g., 2020-23, 2021-24, etc.
                * semester (int | str):
                    - Student's semester. E.g., 1,2,5 etc. (Between 1 to 6)
                    - string format is recommended.
                * host (str, optional):
                    - Hostname of the database server.
                    - Defaults to the hostname set in the environment variable DBHOST.
                * user (str, optional):
                    - Username of the database server.
                    - Defaults to the username set in the environment variable DBUSERNAME.
                * port (int, optional): 
                    - Port number of the database server.
                    - Defaults to the port number set in the environment variable DBPORT or 3306.
                * password (str, optional):
                    - Password of the database server.
                    - Defaults to the password set in the environment variable DBPASSWORD.
        """

        self.semester = str(semester) if type(semester) == int else semester

        # trying to establish connection with the database.
        try:
            self.conn = mysql.connect(
                host=host, user=user, port=port, password=password)
            self.cursor = self.conn.cursor(buffered=True)

            database = f"rdsbca${session}"
            self.cursor.execute(f"""-- sql
                                    USE `{database}`
                                """)
            self.connectionStatus = True  # flag to check if connection is established or not
            print(f"Connection established with the database {database}.")
        except Exception as e:
            print(
                f"Unable to connect with the database {database}. Error code 1400")
            print("Exception:", e)
            self.connectionStatus = False  # if connection not established

    def __del__(self):
        """
            Description:
                - To close the database connection when destructor called.
        """
        if self.connectionStatus:
            self.conn.close()

    def __fetchAllData(self, registrationNo: str) -> dict | None:
        """
            Description:
                - To fetch all result related data only using registrationNo.

            Args:
                * registrationNo (str):
                    - RegistrationNo of student.

            Returns:
                * dict:
                        - If data found on given constraints.
                        - Dictionary containing all desired values with respective keys.
                * None:
                        - In case of any failure.
                        - If data not found in database.
                        - In case of invalid credentials
        """
        attributes = ('Name', 'ExamRoll', 'ClassRoll',
                      'TotalMarks', 'ResultStatus')
        try:
            self.cursor.execute(f"""-- sql
                                    SELECT {attributes[0]},{attributes[1]},{attributes[2]},{attributes[3]},{attributes[4]}
                                    FROM (SELECT * FROM students JOIN result_sem{self.semester} WHERE result_sem{self.semester}.RegistrationNo = students.RegistrationNo)
                                    WHERE RegistrationNo='{registrationNo}'
                                    """)
        except Exception as e:
            print(e)
            print(
                "Error code 1401: Unable to fetch data from the database using registration number.")
            return None

        data = self.cursor.fetchone()  # fetching the desired tuple
        if data is None:  # if no data found on given constraints
            return None
        else:
            requiredData = {}
            requiredData['Semester'] = int(self.semester)
            for index, value in enumerate(data):
                requiredData[attributes[index]] = value
            requiredData['RegistrationNo'] = registrationNo

            return requiredData

    def getResult(self, registrationNo: str = None, examRoll: int = None, classRoll: int = None) -> dict | None:
        """
            Description:
                - To fetch result of students using different parameters (registrationNo, examRoll, classRoll).
                - At least one of the parameters in (registrationNo, examRoll, classRoll) must be given.

            Args:
                * registrationNo (str, optional):
                    - For registration number of student.
                    - Defaults to None.
                * examRoll (int, optional):
                    - For exam roll number of student.
                    - Defaults to None.
                * classRoll (int, optional):
                    - For class roll number of student.
                    - Defaults to None.

            Returns:
                * dict:
                    - If data found on given constraints.
                    - Dictionary containing all desired values with respective keys.
                * None:
                    - In case of any failure.
                    - If data not found in database.
                    - In case of invalid credentials
        """
        if registrationNo:
            return self.__fetchAllData(registrationNo)

        # Now, if registrationNo is not given, then we will search for examRoll and classRoll
        key = ('ExamRoll', 'ClassRoll')
        value = (examRoll, classRoll)

        # Using dictionary comprehension to get the index of the value which is not None instead of using if-else.
        id: dict = {name: id for (name, id) in zip(
            key, value) if id is not None}

        try:
            if id != {}:
                self.cursor.execute("""-- sql
                                        SELECT RegistrationNo FROM students 
                                        WHERE {list(id.keys())[0]}=%s
                                    """, (list(id.values())[0],))

                registrationNo = self.cursor.fetchall()[0][0]
                if registrationNo:
                    return self.__fetchAllData(registrationNo)
        except Exception as e:
            print(e)
            print("Error code 1402: Unable to fetch data from the database using exam roll number or class roll number.")
            print(
                "At least one of the parameters (registrationNo, examRoll, classRoll) is required.")
            print("Invalid credentials or required parameters are not given.")
            return None

        return None


if __name__ == '__main__':
    obj = Result('2020-23', 2)
    print(obj.getResult(examRoll=211084))


# fetchall() return list of tuples on success(data found) and empty list on failure(data not found)
