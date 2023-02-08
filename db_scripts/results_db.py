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

import os
import sqlite3 as sqlite


class Result:
    """
        @description:
            - Class to handle database operations for student's result.

        @methods:
            * getResult():
                - To fetch result of students using various methods (using registrationNo, examRoll, classRoll).
    """

    def __init__(self, session: str, semester: int) -> None:
        """
            Description:
                - To initialize the database connection and cursor using student's session and semester.

            Args:
                * session (str):
                    - Student's session. E.g., 2020-23, 2021-24, etc.
                * semester (int):
                    - Student's semester. E.g., 1,2,5 etc. (Between 1 to 6)
        """
        self.session = session
        self.semester = semester
        try:
            if not os.path.exists(os.getcwd() + f"/database/{session}.db"):
                raise Exception("Invalid database name.")
            self.conn = sqlite.connect(f"database/{session}.db")
            self.cursor = self.conn.cursor()
            self.connectionStatus = True  # flag to check if connection is established or not
        except Exception as e:
            print(
                f"Unable to connect with the database of session {session}. Error code 1400")
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
        attributes = ('Name', 'examRoll', 'classRoll',
                      'TotalMarks', 'ResultStatus')
        try:
            data = self.cursor.execute(
                f"SELECT {attributes[0]},{attributes[1]},{attributes[2]},{attributes[3]},{attributes[4]} FROM (SELECT * FROM Students JOIN ResultSem{self.semester} WHERE ResultSem{self.semester}.registrationNo = Students.registrationNo) WHERE RegistrationNo=?", (registrationNo,)).fetchall()
        except Exception as e:
            print(e)
            return None

        if data == []:  # if no data found on given constraints
            return None
        else:
            requiredData = {}
            requiredData['Semester'] = int(self.semester)
            for index, value in enumerate(data[0]):
                requiredData[attributes[index]] = value

            return requiredData

    def getResult(self, registrationNo: str = None, examRoll: int = None, classRoll: int = None) -> dict | None:
        """
            Description:
                - To fetch result of students using different parameters (registrationNo, examRoll, classRoll).

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
        key = ('examRoll', 'classRoll')
        value = (examRoll, classRoll)

        # Using dictionary comprehension to get the index of the value which is not None instead of using if-else.
        id: dict = {name: id for (name, id) in zip(
            key, value) if id is not None}

        try:
            if id != {}:
                registrationNo = self.cursor.execute(
                    f"SELECT registrationNo FROM Students WHERE {list(id.keys())[0]}=?", (list(id.values())[0],)).fetchall()[0][0]
                if registrationNo:
                    return self.__fetchAllData(registrationNo)
        except Exception as e:
            print(e)
            return None

        return None


if __name__ == '__main__':
    obj = Result('2020-23', 2)
    print(obj.getResult(examRoll=211084))


# fetchall() return list of tuples on success(data found) and empty list on failure(data not found)
