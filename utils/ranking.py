import sqlite3

from tabulate import tabulate


class RankingSystemDB:
    def __init__(self, db_name="results/rankings.db"):
        self.connection = sqlite3.connect(db_name)
        self.__create_table()

    def __create_table(self):
        with self.connection:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS rankings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    algorithm_name TEXT UNIQUE,
                    point INTEGER,
                    total_point INTEGER,
                    average_time_s REAL,
                    testcase_name TEXT
                )
            """
            )

    def add_entry(
        self, algorithm_name, point, total_point, average_time_s, testcase_name
    ):
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO rankings (algorithm_name, point, total_point, average_time_s, testcase_name)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(algorithm_name)
                DO UPDATE SET
                    point = excluded.point,
                    total_point = excluded.total_point,
                    average_time_s = excluded.average_time_s,
                    testcase_name = excluded.testcase_name;
            """,
                (algorithm_name, point, total_point, average_time_s, testcase_name),
            )

    def display_ranks(self):
        cursor = self.connection.execute(
            """
            SELECT ROW_NUMBER() OVER (ORDER BY (CAST(point AS FLOAT) / total_point) DESC, average_time_s ASC) AS rank,
                algorithm_name,
                printf('%d/%d', point, total_point) AS points,
                ROUND((CAST(point AS FLOAT) / total_point) * 100, 2) AS percentage,
                average_time_s,
                testcase_name
            FROM rankings
            ORDER BY percentage ASC, average_time_s DESC
        """
        )
        rows = cursor.fetchall()
        headers = [
            "Rank",
            "Algorithm Name",
            "Point/Total Point",
            "Percentage (%)",
            "Average Time (s)",
            "Test Case Name",
        ]
        print(
            tabulate(
                rows,
                headers=headers,
                tablefmt="grid",
                floatfmt=["", "", "", ".2f", ".5f", ""],
            )
        )


if __name__ == "__main__":
    ranking_system_db = RankingSystemDB()
    ranking_system_db.add_entry("Algorithm A", 80, 80, 0.1500, "Dataset 1")
    ranking_system_db.add_entry("Algorithm B", 90, 110, 0.1200, "Dataset 1")
    ranking_system_db.add_entry("Algorithm C", 90, 110, 0.1500, "Dataset 1")
    ranking_system_db.display_ranks()
