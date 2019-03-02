from fuzzywuzzy import fuzz, process
from nltk import stopwords


def get_from_db(parameter, database_info:dict):
	choices = list(database_info)
	db_col = process.extractOne(parameter, choices)[0]
	return database_info[db_col]


def process_query(query):
	query_parts = [word for word in query if ]

db = {"loan_amt":"654", "acc_balance":"100000"}

print(get_from_db("loan amount", db))
