"""
    @author: Suraj Kumar Giri
    @date: 17th Oct 2022
    @description:
        * Module to handle database operations.
"""

__author__ = 'Suraj Kumar Giri'
__email__ = 'surajgirioffl@gmail.com'

import sqlite3 as sqlite


class StudentDetails:
    ...


class Result:
    def __init__(self, session: str, semester: int) -> None:
        self.session = session
        self.semester = semester
        self.conn = sqlite.connect(f"database/{session}.db")
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def __fetchAllData(self, registrationNo: str) -> dict | None:
        attributes = ('Name', 'examRoll', 'classRoll',
                      'TotalMarks', 'ResultStatus')
        data = self.cursor.execute(
            f"SELECT {attributes[0]},{attributes[1]},{attributes[2]},{attributes[3]},{attributes[4]} FROM (SELECT * FROM Students JOIN ResultSem{self.semester} WHERE ResultSem{self.semester}.registrationNo = Students.registrationNo) WHERE RegistrationNo=?", (registrationNo,)).fetchall()

        if data == []:  # if no data found on given constraints
            return None
        else:
            requiredData = {}
            for index, value in enumerate(data[0]):
                requiredData[attributes[index]] = value
            return requiredData

    def getResult(self, registrationNo: str = None, examRoll: int = None, classRoll: int = None) -> dict | None:
        if registrationNo:
            return self.__fetchAllData(registrationNo)

        # Now, if registrationNo is not given, then we will search for examRoll and classRoll
        key = ('examRoll', 'classRoll')
        value = (examRoll, classRoll)

        # Using dictionary comprehension to get the index of the value which is not None instead of using if-else.
        id: dict = {name: id for (name, id) in zip(
            key, value) if id is not None}

        if id != {}:
            registrationNo = self.cursor.execute(
                f"SELECT registrationNo FROM ResultSem{self.semester} WHERE {list(id.keys())[0]}=?", (list(id.values())[0],)).fetchall()[0][0]
            if registrationNo:
                return self.__fetchAllData(registrationNo)
        return None


if __name__ == '__main__':
    obj = Result('2020-23', 2)
    print(obj.getResult(examRoll=211084))


# fetchall() return list of tuples on success(data found) and empty list on failure(data not found)
