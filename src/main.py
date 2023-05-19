import os
from utils import dumpJsonFile, loadJsonFile
import sqlite3
import pandas as pd
from text_sim import *
from tqdm import tqdm
import time

import warnings
warnings.filterwarnings('ignore')


from typing import List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# Model taken from Huggingface Github Repo
MODEL_PATH = "juierror/flan-t5-text2sql-with-schema"
TOKENIZER_PATH = "juierror/flan-t5-text2sql-with-schema"
COLUMNS_JSON_FILE = "/Users/niravdiwan/Desktop/projects/text2sql/text2sql-LLM/data/columns.json"

def prepare_input(question: str, table: List[str]):
    table_prefix = "table:"
    table_name_prefix = "table_name:"
    sample_prefix = ""
    question_prefix = "question:"
    join_table = ",".join(table)
    inputs = f"""
    You are an SQL Query expert who can write SQL queries for the below table.

    {table_prefix} {join_table}

    Answer the following question:
    question : {question}
    """
    # print("\t ---- Prompt ----- \t")
    # print(inputs)

    input_ids = tokenizer(inputs, max_length=512, return_tensors="pt").input_ids
    return input_ids


def cot_prepare_input(question: str, table: List[str], questions : List[str], example_queries : List[str]):
    table_prefix = "table:"
    table_name_prefix = "table_name:"
    sample_prefix = ""
    question_prefix = "question:"
    join_table = ",".join(table)
    inputs = f"""
    You are an SQL Query expert who can write SQL queries for the below table.
    {table_prefix} {join_table}
    For the below questions, you are given the example queries. You need to write the SQL query for the last question.
    """

    for question_no, s_question in enumerate(questions):
        inputs += f"""
        {s_question}
        {example_queries[question_no]}
        """

    inputs += f"""
    Only answer the following question:
    {question},
    """

    input_ids = tokenizer(inputs, max_length=512, return_tensors="pt").input_ids
    return input_ids


def inference(question: str, table: List[str]) -> str:
    input_data = prepare_input(question=question, table=table)
    input_data = input_data.to(model.device)
    outputs = model.generate(inputs=input_data, num_beams=10, top_k=10, max_length=1024)
    result = tokenizer.decode(token_ids=outputs[0], skip_special_tokens=True)
    return result

def cot_inference(question: str, table: List[str], questions : List[str], example_queries : List[str]) -> str:
    input_data = cot_prepare_input(question=question, table=table, questions = questions, example_queries = example_queries)
    input_data = input_data.to(model.device)
    outputs = model.generate(inputs=input_data, num_beams=10, top_k=10, max_length=1024)
    result = tokenizer.decode(token_ids=outputs[0], skip_special_tokens=True)
    return result



def test(question, DB_FILEPATH = "../data/database/final_db.db", k = 5, table_name = "employee"):

    # Retrive the samples
    test_df = pd.read_csv("../data/example_queries/test_set/final_" +  table_name  + ".csv", delimiter="|")
    retr_df = pd.read_csv("../data/example_queries/retr_set/final_" +  table_name  + ".csv", delimiter="|")

    sample_questions = []
    sample_queries = []

    print("\n")

    for index, row in retr_df.iterrows():
        s_question = row["Question"]
        sql_query = row["SQL Query"]
        sample_questions.append(s_question)
        sample_queries.append(sql_query)

    print("Loading SQL Database ...")
    conn = sqlite3.connect(DB_FILEPATH)
    for i in tqdm(range(2)):
        time.sleep(1)


    print("\n")

    print("Retrieving top " + str(k)  + " similar queries from the dataset to perform Chain of Thought (CoT) Prompting ...")
    top_k_indices = get_top_k_similar(question, sample_questions, k = k)

    sample_questions = [sample_questions[i] for i in top_k_indices]
    sample_queries = [sample_queries[i] for i in top_k_indices]

    for question_no, s_question in enumerate(sample_questions):
        print("Question : ", sample_questions[question_no])
        print("SQL Query :", sample_queries[question_no])

    print("\n")

    # print(" ========= Zero-Shot Test SQL ========= ")
    gen_query1 = inference(question, table)
    gen_query1 = gen_query1.replace(" table", " " + table_name)
    
    print("Generated Query using Zero-Shot Prompting = ", gen_query1)
    try:
        print(conn.execute(gen_query1).fetchall())
        print("Zero-Shot Query Works!")
    except:
        print("Error in Zero-Shot SQL Query")

    # print(" ========= CoT Test SQL ========= ")
    gen_query2 = cot_inference(question, table, sample_questions, sample_queries)
    gen_query2 = gen_query2.replace(" table", " " + table_name)
    
    print("Generated Query using Chain of Thought (CoT) Prompting = ", gen_query2)
    try:
        print(conn.execute(gen_query2).fetchall())
        print("CoT Query Works!")
    except:
        print("Error in CoT SQL Query!")



def test_dataset(DB_FILEPATH = "../data/database/final_db.db", k = 5, table_name = "employee"):

    test_df = pd.read_csv("../data/example_queries/test_set/final_" +  table_name  + ".csv", delimiter="|")
    retr_df = pd.read_csv("../data/example_queries/retr_set/final_" +  table_name  + ".csv", delimiter="|")

    sample_questions = []
    sample_queries = []


    print("\n")

    for index, row in retr_df.iterrows():
        s_question = row["Question"]
        sql_query = row["SQL Query"]
        sample_questions.append(s_question)
        sample_queries.append(sql_query)

    print("Loading SQL Database ...")
    conn = sqlite3.connect(DB_FILEPATH)
    for i in tqdm(range(2)):
        time.sleep(1)

    for index, row in test_df.iterrows():
        print("\n\n\n\n\n")
        print(" ========= Test Query ========= ")
        question = row["Question"]

        top_k_indices = get_top_k_similar(question, sample_questions, k=5)

        print("Loading Sample ")

        sample_questions = [sample_questions[i] for i in top_k_indices]
        sample_queries = [sample_queries[i] for i in top_k_indices]

        print("Sample Questions = ", sample_questions)
        print("Sample Queries = ", sample_queries)

        print(" ========= Zero-Shot Test SQL ========= ")
        sql_query = row["SQL Query"]
        gen_query = inference(question, table)
        gen_query = gen_query.replace(" table", " " + table_name)
        print("Generated Query = ", gen_query)
        print("Original Query = ", sql_query)
        try:
            print(conn.execute(gen_query).fetchall())
        except:
            print("Error in SQL Query")


        print("\n\n\n\n\n")

        print(" ========= CoT Test SQL ========= ")
        gen_query = cot_inference(question, table, sample_questions, sample_queries)
        gen_query = gen_query.replace(" table", " " + table_name)
        print("Generated Query = ", gen_query)
        print("Original Query = ", sql_query)
        try:
            print(conn.execute(gen_query).fetchall())
        except:
            print("Error in SQL Query")

    conn.close()



print("\n\n\n")
print("Hi! I am a SQL Query Generator. I can generate SQL queries for you. Please enter the table name for which you want to generate the SQL query.")
table_name = input("Enter the table name : ")

columns = loadJsonFile("../data/columns.json", verbose=False)
table = columns[table_name]

print("\n")

print("Loading the model ...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSeq2SeqLM.from_pretrained(TOKENIZER_PATH)

test_bool = input("Do you want to enter your own question (y) or perform an evaluation on the test dataset (n) ?")

print("\n")

if test_bool == "y":
    question = input("Enter your question : ")
    test(question, DB_FILEPATH = "../data/database/final_db.db", k = 5, table_name = table_name)
else:
    test_dataset(DB_FILEPATH = "../data/database/final_db.db", k = 5, table_name = table_name)