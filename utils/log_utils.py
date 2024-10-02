import json
import sqlite3
from datetime import datetime, timedelta, timezone

from tabulate import tabulate


class LoggingSystemDB:
    def __init__(self, db_name="logs/loggings.db"):
        self.connection = sqlite3.connect(db_name)
        self.__create_table()

    def __create_table(self):
        with self.connection:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS loggings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    algorithm_name TEXT,
                    answer TEXT,
                    correct_answer TEXT,
                    answer_status TEXT,
                    time_s REAL,
                    testcase_name TEXT,
                    created_at TEXT
                )
            """
            )

    def add_entry(
        self,
        algorithm_name,
        answer,
        correct_answer,
        answer_status,
        time_s,
        testcase_name,
    ):
        vietnam_time = (datetime.now(timezone.utc) + timedelta(hours=7)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO loggings (algorithm_name, answer, correct_answer, answer_status, time_s, testcase_name, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    algorithm_name,
                    answer,
                    correct_answer,
                    answer_status,
                    time_s,
                    testcase_name,
                    vietnam_time,
                ),
            )

    def __print_comparison(
        self,
        algorithm_name,
        answer,
        correct_answer,
        answer_status,
        time_s,
        testcase_name,
        create_at,
    ):
        answer = json.loads(answer)
        correct_answer = json.loads(correct_answer)

        comparison_data = []
        for key in answer.keys():
            comparison_data.append([key, answer[key], correct_answer[key]])

        print(f"Algorithm Name: {algorithm_name}")
        print(f"Test Case Name: {testcase_name}")
        print(f"Answer Status: {answer_status}")
        print(f"Run Time (s): {time_s:.5f}")
        print(f"Create At: {create_at}")

        headers = ["Key", "Answer", "Correct Answer"]
        print(tabulate(comparison_data, headers=headers, tablefmt="grid"))

    def display_logs(self, answer_status=""):
        query = """
            SELECT algorithm_name,
                answer,
                correct_answer,
                answer_status,
                time_s,
                testcase_name,
                created_at
            FROM loggings
        """
        if answer_status in ["correct", "incorrect"]:
            query += " WHERE LOWER(answer_status) = ?"
            cursor = self.connection.execute(
                query + " ORDER BY created_at ASC", (answer_status,)
            )
        else:
            cursor = self.connection.execute(query + " ORDER BY created_at ASC")

        rows = cursor.fetchall()
        for row in rows:
            self.__print_comparison(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6]
            )
            print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    logging_system_db = LoggingSystemDB()
    # logging_system_db.add_entry("Algorithm A", '{"ward":"Tân Chánh Hiệp","district":"12","province":"Hồ Chí Minh"}', '{"ward":"Tân Chánh Hiệp","district":"12","province":"Hồ Chí Minh"}', "Incorrect", 0.1500, "Dataset 1")
    # logging_system_db.add_entry("Algorithm B", '{"ward":"Tân Chánh Hiệp","district":"12","province":"Hồ Chí Minh"}', '{"ward":"Tân Chánh Hiệp","district":"12","province":"Hồ Chí Minh"}', "Incorrect", 0.1200, "Dataset 1")
    logging_system_db.display_logs(answer_status="correct")
