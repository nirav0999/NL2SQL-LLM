import json
import csv
import collections
import pickle
import os
import sqlite3

#-------------------------JSON Functions-------------------------------------------------------
def dumpJsonFile(dictionary, filepath, verbose = True, print_dict = False):
	"""
	Dump a json file
	"""
	if verbose == True : print("Dumping a dictionary to filepath",filepath,"...............")
	
	with open(filepath,"w+") as jsonFile:
		json.dump(dictionary, jsonFile, indent = 4, sort_keys = True)
	
	if print_dict == True : print(json.dumps(dictionary,indent = 4))
	if verbose == True : print("Dumped Successfully")


def loadJsonFile(filepath, verbose = True, print_dict = False):
	"""
	Load a json file 
	"""
	if verbose == True : print("Loading a dictionary to filepath",filepath,".........")
	dictionary = {}
	
	with open(filepath) as jsonFile:
		dictionary = json.load(jsonFile)
	
	if verbose == True : print("Loaded Successfully")
	if print_dict == True : print(json.dumps(dictionary,indent = 4))

	return dictionary

def createSQLDB(db_path, sql_path):
    """
    Create a SQL database from a SQL file
    """
    conn = sqlite3.connect(db_path)
    with open(sql_path, 'r') as sql_file:
        conn.executescript(sql_file.read())
    conn.close()

if __name__ == "__main__":
	pass