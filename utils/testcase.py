import json
import os
import random
import time
from datetime import datetime, timedelta, timezone

import pandas as pd
from tqdm import tqdm

from utils.database import Database
from utils.log_utils import LoggingSystemDB
from utils.ranking import RankingSystemDB


class TestCase:
    def __init__(self, path="testcases/", db_path="datas/database/database.csv"):
        self.path = path
        if not os.path.isfile(db_path):
            database = Database()
            database.extract_data_to_csv()
        self.df = pd.read_csv(db_path)
        self.df.rename(
            columns={
                "Tên": "Phường_xã",
                "Quận Huyện": "Quận_huyện",
                "Tỉnh / Thành Phố": "Tỉnh_thành_phố",
            },
            inplace=True,
        )
        self.df = self.df.fillna("")

    def __rand_testcase(self, testcase_num=10):
        df_rand = self.df.copy()
        df_rand = df_rand.sample(n=testcase_num, replace=True)
        return df_rand

    def __rand_vn_char(self):
        vn_alphabet = [
            # Uppercase letters
            "A",
            "Ă",
            "Â",
            "B",
            "C",
            "D",
            "Đ",
            "E",
            "Ê",
            "G",
            "H",
            "I",
            "K",
            "L",
            "M",
            "N",
            "O",
            "Ô",
            "Ơ",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "Ư",
            "V",
            "X",
            "Y",
            # Lowercase letters
            "a",
            "ă",
            "â",
            "b",
            "c",
            "d",
            "đ",
            "e",
            "ê",
            "g",
            "h",
            "i",
            "k",
            "l",
            "m",
            "n",
            "o",
            "ô",
            "ơ",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "ư",
            "v",
            "x",
            "y",
        ]

        # Diacritics (tones) combinations for vowels
        vn_accent = [
            # A, Â, Ă variants
            "À",
            "Á",
            "Ả",
            "Ã",
            "Ạ",
            "Ầ",
            "Ấ",
            "Ẩ",
            "Ẫ",
            "Ậ",
            "Ằ",
            "Ắ",
            "Ẳ",
            "Ẵ",
            "Ặ",
            "È",
            "É",
            "Ẻ",
            "Ẽ",
            "Ẹ",
            "Ề",
            "Ế",
            "Ể",
            "Ễ",
            "Ệ",  # E, Ê variants
            "Ì",
            "Í",
            "Ỉ",
            "Ĩ",
            "Ị",  # I variants
            # O, Ô, Ơ variants
            "Ò",
            "Ó",
            "Ỏ",
            "Õ",
            "Ọ",
            "Ồ",
            "Ố",
            "Ổ",
            "Ỗ",
            "Ộ",
            "Ờ",
            "Ớ",
            "Ở",
            "Ỡ",
            "Ợ",
            "Ù",
            "Ú",
            "Ủ",
            "Ũ",
            "Ụ",
            "Ừ",
            "Ứ",
            "Ử",
            "Ữ",
            "Ự",  # U, Ư variants
            "Ỳ",
            "Ý",
            "Ỷ",
            "Ỹ",
            "Ỵ",  # Y variants
            # a, â, ă variants
            "à",
            "á",
            "ả",
            "ã",
            "ạ",
            "ầ",
            "ấ",
            "ẩ",
            "ẫ",
            "ậ",
            "ằ",
            "ắ",
            "ẳ",
            "ẵ",
            "ặ",
            "è",
            "é",
            "ẻ",
            "ẽ",
            "ẹ",
            "ề",
            "ế",
            "ể",
            "ễ",
            "ệ",  # e, ê variants
            "ì",
            "í",
            "ỉ",
            "ĩ",
            "ị",  # i variants
            # o, ô, ơ variants
            "ò",
            "ó",
            "ỏ",
            "õ",
            "ọ",
            "ồ",
            "ố",
            "ổ",
            "ỗ",
            "ộ",
            "ờ",
            "ớ",
            "ở",
            "ỡ",
            "ợ",
            "ù",
            "ú",
            "ủ",
            "ũ",
            "ụ",
            "ừ",
            "ứ",
            "ử",
            "ữ",
            "ự",  # u, ư variants
            "ỳ",
            "ý",
            "ỷ",
            "ỹ",
            "ỵ",  # y variants
        ]

        full_vn_alphabet = vn_alphabet + vn_accent
        return random.choices(full_vn_alphabet)

    def __substitute_char(self, value):
        value_list = list(value)
        length = len(value_list)

        rand_position = random.randint(0, length - 1)
        value_list[rand_position] = random.choice(self.__rand_vn_char())
        return "".join(value_list)

    def __delete_char(self, value):
        value_list = list(value)
        length = len(value_list)

        rand_position = random.randint(0, length - 1)
        value_list[rand_position] = ""
        return "".join(value_list)

    def __add_char(self, value):
        value_list = list(value)
        length = len(value_list)

        rand_position = random.randint(0, length + 1)
        added_list = (
            "".join(value_list[:rand_position])
            + "".join(random.choice(self.__rand_vn_char()))
            + "".join(value_list[rand_position:])
        )
        return added_list

    def __rand_edit_word(self, value, error_percent):
        length = len(value)
        num_char_edit = random.randint(0, round(length * error_percent / 100))
        functions = [self.__substitute_char, self.__delete_char, self.__add_char]
        for _ in range(num_char_edit):
            random_function = random.choice(functions)
            value = random_function(value)
        return value

    def generate_testcase(self, testcase_num=10, error_percent=10):
        df_sample = self.__rand_testcase(testcase_num)
        df_edit = df_sample.copy()
        df_edit = df_edit.map(lambda x: self.__rand_edit_word(x, error_percent))

        corrected = []
        for _, rows in df_sample.iterrows():
            corrected_record = (
                rows["Phường_xã"],
                rows["Quận_huyện"],
                rows["Tỉnh_thành_phố"],
            )
            corrected.append(corrected_record)

        inputs = []
        for _, rows in df_edit.iterrows():
            input_record = (
                rows["Phường_xã"],
                rows["Quận_huyện"],
                rows["Tỉnh_thành_phố"],
            )
            inputs.append(input_record)

        combined_template = []
        for i in range(len(inputs)):
            template = {
                "input_address": inputs[i][0]
                + ", "
                + inputs[i][1]
                + ", "
                + inputs[i][2],
                "output": {
                    "ward": corrected[i][0],
                    "district": corrected[i][1],
                    "province": corrected[i][2],
                },
            }

            combined_template.append(template)

        formatted_time = (datetime.now(timezone.utc) + timedelta(hours=7)).strftime(
            "%Y%m%d_%H%M%S"
        )
        file_name = f"testcase_{formatted_time}.json"
        with open(
            os.path.join(self.path, file_name), "w", encoding="utf-8"
        ) as json_file:
            json.dump(combined_template, json_file, ensure_ascii=False, indent=4)
        return file_name

    def display_testcase(self, testcase_file_name):
        with open(
            os.path.join(self.path, testcase_file_name), "r", encoding="utf-8"
        ) as f:
            testcases = json.load(f)
        print(json.dumps(testcases, indent=4, ensure_ascii=False))

    def run_testcase(
        self,
        algorithm_name,
        func,
        testcase_file_name,
        time_limit=0.2,
        average_time_limit=0.04,
    ):
        with open(
            os.path.join(self.path, testcase_file_name), "r", encoding="utf-8"
        ) as f:
            testcases = json.load(f)
        total_testcase = len(testcases)
        total_elapsed_time = 0
        point = 0
        logging = LoggingSystemDB()
        for testcase in tqdm(testcases, desc="Processing"):
        # for testcase in testcases:
            start_time = time.time()
            answer = func(testcase["input_address"])
            end_time = time.time()

            if not isinstance(answer, dict):
                raise TypeError(
                    f"Expected answer a dictionary, but got {type(answer).__name__} instead."
                )

            elapsed_time = round(end_time - start_time, 5)
            total_elapsed_time += elapsed_time
            answer_status = "Incorrect"
            if answer == testcase["output"]:
                point += 1
                answer_status = "Correct"
            answer = json.dumps(answer, ensure_ascii=False)
            correct_answer = json.dumps(testcase["output"], ensure_ascii=False)
            logging.add_entry(
                algorithm_name,
                answer,
                correct_answer,
                answer_status,
                elapsed_time,
                testcase_file_name,
            )
            if elapsed_time > time_limit:
                point = 0
                break
        average_elapsed_time = round((total_elapsed_time / total_testcase), 5)
        if average_elapsed_time > average_time_limit:
            point = 0
        ranking = RankingSystemDB()
        ranking.add_entry(
            algorithm_name,
            point,
            total_testcase,
            average_elapsed_time,
            testcase_file_name,
        )


if __name__ == "__main__":

    def test(input):
        return {
            "ward": "Đông Phương Yên",
            "district": "Chương Mỹ",
            "province": "Hà Nội",
        }

    testcase = TestCase()
    # testcase.generate_testcase(error_percent=10)
    # testcase.run_testcase(algorithm=test, testcase_file_name='testcase_20241002_013436.json')
