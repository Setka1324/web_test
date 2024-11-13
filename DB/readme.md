Not a proper MD file, but better then nothing

Also don't have time for a proper requirments autocheck and start file:
sqlite3
json
pandas
csv
io
uuid
flask

To start: "flask run --debug" from web folder

ERD in DB
Project Description and Tracking reflections aree in static.

create_db.py : just makes a database
find attributes : Used to understand the structure
transfer_data_json : transfers data from json and fixes a lot of typos/issues
transfer_data_csv : transfers data from csv and fixes a some typos/issues
clean_techs : cleans up inconsistances with naming of technology in dataset
sql.sql : just for some testing


Tried to leave comments or at least generate them with gpt, so it is easier to read. But was in a hurry, so they are not everywhere. Sorry. It is also a bit messy in the structure

Testiing recommendations:

For "Compliance" check those companies. External links sometimes lead to nothing, but that a dataset issue, not mine.
Area
Wipro Technologies
Yaana

For "Map":
Filters show companies that have at least one of the filters, and it may lag if you have bad connection

For "News":
Dataset didn't really have many countries, but it should work good for existing ones.

Important!!!:
I used my personal key for the map API and I hope that you will not use it or show it to anyone