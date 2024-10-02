import os

import pandas as pd


class Database:
    def __init__(
        self,
        excel_file="data/origin/Danh sách cấp xã ___25_09_2024.xls",
        path="data/database/",
    ):
        self.excel_file = excel_file
        self.path = path

    def __preprocess_df(self, df):
        city_prefix = {"Thành phố": "", "Tỉnh": ""}
        df["Tỉnh / Thành Phố"] = (
            df["Tỉnh / Thành Phố"].replace(city_prefix, regex=True).str.strip()
        )

        district_prefix = {
            "Quận": "",
            "Huyện": "",
            "Thị xã": "",
            "Thành phố": "",
            "Thị Xã": "",
            "Thành Phố": "",
        }
        df["Quận Huyện"] = (
            df["Quận Huyện"].replace(district_prefix, regex=True).str.strip()
        )

        ward_prefix = {"Phường": "", "Thị trấn": "", "Xã": "", "Thị Trấn": ""}
        df["Tên"] = df["Tên"].replace(ward_prefix, regex=True).str.strip()
        return df

    def extract_data_to_text(self):
        df = pd.read_excel(self.excel_file)
        df = self.__preprocess_df(df)

        pd.DataFrame(
            df["Tỉnh / Thành Phố"].unique(), columns=["Tỉnh / Thành Phố"]
        ).to_csv(
            os.path.join(self.path, "list_province.txt"), index=False, header=False
        )
        pd.DataFrame(df["Quận Huyện"].unique(), columns=["Quận Huyện"]).to_csv(
            os.path.join(self.path, "list_district.txt"), index=False, header=False
        )
        pd.DataFrame(df["Tên"].unique(), columns=["Tên"]).to_csv(
            os.path.join(self.path, "list_ward.txt"), index=False, header=False
        )

    def extract_data_to_csv(self, csv_name="database.csv"):
        df = pd.read_excel(self.excel_file)
        df = self.__preprocess_df(df)
        df[["Tên", "Quận Huyện", "Tỉnh / Thành Phố"]].to_csv(
            os.path.join(self.path, csv_name), index=False, encoding="utf-8-sig"
        )

    def read_text_db(self, db_name):
        file_path = f"datas/database/{db_name}.txt"
        lines_list = []
        with open(file_path, "r") as file:
            lines_list = file.readlines()
        lines_list = [line.strip() for line in lines_list]
        return lines_list


if __name__ == "__main__":
    database = Database()
    database.extract_data_to_text()
    database.extract_data_to_csv()
