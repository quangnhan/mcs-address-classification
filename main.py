import time

from database import ProvinceDB, DistrcitDB, WardDB
from search_strategy import ExactMatchStrategy, TrieStrategy
start = time.time()

# Load database
province_db = ProvinceDB()
district_db = DistrcitDB()
ward_db = WardDB()

province_db.load()
load_province_db_end_time = time.time()

district_db.load()
load_district_db_end_time = time.time()

ward_db.load()
load_ward_db_end_time = time.time()

# Create searching instant
search_strategy_cls = ExactMatchStrategy

province_search_strategy = search_strategy_cls(province_db.location_mapping.keys())
create_searching_instant_province_end_time = time.time()

district_search_strategy = search_strategy_cls(district_db.location_mapping.keys())
create_searching_instant_district_end_time = time.time()

ward_search_strategy = search_strategy_cls(ward_db.location_mapping.keys())
create_searching_instant_ward_end_time = time.time()

# Preprocessing input
input = "Xã Đất Mũi , Huyện Ngọc Hiển, Tỉnh Cà Mau"
province = "tỉnh cà mau"
district = "huyện ngọc hiển"
ward = "xã đất mũi"

print(province_db.location_mapping)
# Searching
final_province = province_search_strategy.search(province)
search_province_end_time = time.time()

final_district = district_search_strategy.search(district)
search_district_end_time = time.time()

final_ward = ward_search_strategy.search(ward)
search_ward_end_time = time.time()

# Search for word
#####################################################
print(f"Load province DB: {load_province_db_end_time - start}")
print(f"Load district DB: {load_district_db_end_time - load_province_db_end_time}")
print(f"Load ward DB: {load_ward_db_end_time - load_district_db_end_time}")
print("---------------------------------------")
print(f"Create searching instant province DB: {create_searching_instant_province_end_time - load_ward_db_end_time}")
print(f"Create searching instant district DB: {create_searching_instant_district_end_time - create_searching_instant_province_end_time}")
print(f"Create searching instant ward DB: {create_searching_instant_ward_end_time - create_searching_instant_district_end_time}")
print("---------------------------------------")
print(f"Searching province DB: {search_province_end_time - create_searching_instant_ward_end_time}")
print(f"Searching district DB: {search_district_end_time - search_province_end_time}")
print(f"Searching ward DB: {search_ward_end_time - search_district_end_time}")
print("---------------------------------------")
print(f"Final province: {final_province}")
print(f"Final district: {final_district}")
print(f"Final ward: {final_ward}")
print(f"Total: {search_ward_end_time - start}")