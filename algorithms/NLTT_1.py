from rapidfuzz import process

from utils.database import Database


def run_algorithm(_input):
    # print("Running Algorithm 1")
    # Algorithm logic here
    database = Database()
    list_province = database.read_text_db(db_name="list_province")
    list_district = database.read_text_db(db_name="list_district")
    list_ward = database.read_text_db(db_name="list_ward")
    # best_ward = process.extractOne(_input[(len(_input)*3//5):], list_ward)
    # best_district = process.extractOne(_input, list_district)
    best_province = process.extractOne(_input[-(len(_input) * 3 // 5) :], list_province)

    # print(_input)
    # print(f"Best Ward: {best_ward}")
    # print(f"Best District: {best_district}")
    # print(f"Best Province: {best_province}")
    return {"ward": "Đông Phương Yên", "district": "Chương Mỹ", "province": "Hà Nội"}
