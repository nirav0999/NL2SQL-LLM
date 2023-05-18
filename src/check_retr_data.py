from utils import loadJsonFile, dumpJsonFile
import os
import sqlite3
import pandas as pd
import random

# Table Name
table_name = "group_final"

# Loading SQL Database 
DB_FILEPATH = "../data/database/final_db.db"
conn = sqlite3.connect(DB_FILEPATH)

# Load the example queries
df = pd.read_csv("../data/example_queries/complete_set/" + table_name + ".csv", header="infer", delimiter="|")

final_examples = {}

print(df.columns)

# Check if the query is valid
for index, row in df.iterrows():
    question = row['Question'] 
    query = row['SQL Query']
    print(" ========= SQL Result ========= ")
    try:
        print("Question: ", question)
        print("Query: ", query)
        print(conn.execute(query).fetchall())
        final_examples[question] = query
    except:
        print("Query Failed")

conn.close()

print("Total Number of Sucessful Examples: ", len(final_examples))

final_dataset = []
for example in final_examples:
    final_dataset.append([example, final_examples[example]])

random.shuffle(final_dataset)

# Picking the first 5 examples as test set
test_data = pd.DataFrame(final_dataset[:5], columns = ['Question', 'SQL Query'])

# Picking the rest as retrieval set
retr_data = pd.DataFrame(final_dataset[5:], columns = ['Question', 'SQL Query'])

test_data.to_csv("../data/example_queries/test_set/final_" + table_name + ".csv", sep="|", index=False)
retr_data.to_csv("../data/example_queries/retr_set/final_" + table_name + ".csv", sep="|", index=False)