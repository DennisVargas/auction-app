SET dir_path=.
sqlite3 ./web.py/ebay_data.db < create.sql
sqlite3 ./web.py/ebay_data.db < load.txt
sqlite3 ./web.py/ebay_data.db < constraints_verify.sql
sqlite3 ./web.py/ebay_data.db < trigger1_add.sql
sqlite3 ./web.py/ebay_data.db < trigger2_add.sql
sqlite3 ./web.py/ebay_data.db < trigger3_add.sql
sqlite3 ./web.py/ebay_data.db < trigger4_add.sql
sqlite3 ./web.py/ebay_data.db < trigger5_add.sql
sqlite3 ./web.py/ebay_data.db < trigger6_add.sql
sqlite3 ./web.py/ebay_data.db < trigger7_add.sql
@rem sqlite3 ./web.py/ebay_data.db < trigger8_add.sql
@rem