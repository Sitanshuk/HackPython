from fuzzywuzzy import fuzz, process
from nltk.corpus import stopwords

# used set to improve the lookup time.
stopwords = set(stopwords.words("english"))

def get_from_db(parameter, database_info:dict):
	""" this returns the most relevant param from the database dict."""

	choices = list(database_info) # all the header for the database cols that bot can select.

	db_col = process.extractOne(parameter, choices)[0]     # this will get the most relevant col header for the given param

	# returns the val of the most matching db col.
	return database_info[db_col]


def strip_all(string, weeds=(',', '\\', '/', '"', "'", '.', '?')):
	# removes all the punctuation chars from the given string.
	return "".join([i for i in string if i not in weeds])


def process_query(query):
	query_parts = [strip_all(word) for word in query.split()]
	query_parts = [strip_all(word) for word in query_parts if word not in stopwords]
	return query_parts


print(process_query('what is the loan amount??'))

db = {"loan_amt": "654", "acc_balance": "100000"}

print(get_from_db("loan amount", db))











