import sqlite3 as sqlite


class PreviousYearQuestions:

    def __init__(self, semester: int | str) -> None:
        self.semester = int(semester)
        self.conn = sqlite.connect('database/PreviousYearQuestions.db')
        self.cursor = self.conn.cursor()

    def __del__(self) -> None:
        self.conn.close()

    def getLinks(self, source: str) -> tuple[int, str, str] | None:
        if source == "all":
            data = self.cursor.execute(f"""
                                            SELECT "BRABU" AS Source, Year, Sem{self.semester} FROM brabu WHERE Sem{self.semester} IS NOT NULL UNION
                                            SELECT "Vaishali Institute, Muzaffarpur", Year, Sem{self.semester} AS Source FROM vaishali WHERE Sem{self.semester} IS NOT NULL UNION
                                            SELECT "LN Mishra, Muzaffarpur", Year, Sem{self.semester} as Source FROM lnMishra WHERE Sem{self.semester} IS NOT NULL
                                        """).fetchall()
            return data

        elif source == "brabu":
            data = self.cursor.execute(
                f'SELECT "BRABU" AS Source, Year, Sem{self.semester} FROM brabu WHERE Sem{self.semester} IS NOT NULL').fetchall()
            return data

        elif source == "vaishali":
            data = self.cursor.execute(
                f'SELECT "Vaishali Institute, Muzaffarpur" AS Source, Year, Sem{self.semester} FROM vaishali WHERE Sem{self.semester} IS NOT NULL').fetchall()
            return data

        elif source == "lnMishra":
            data = self.cursor.execute(
                f'SELECT "LN Mishra, Muzaffarpur" as Source, Year, Sem{self.semester} FROM lnMishra WHERE Sem{self.semester} IS NOT NULL').fetchall()
            return data
        else:
            return None


if __name__ == '__main__':
    obj = PreviousYearQuestions(2)
    data = obj.getLinks('all')
    for row in data:
        print(row)
