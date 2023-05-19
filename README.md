# text2sql-LLM
Goal - Retrieving Synthetic data for In-context Learning for Text-to-SQL Generation

1. Check if the queries in the retrieval and test set work - Drop the Queries that don't work
2. Compare the performance of the Independently sample test query and the CoT prompted test query - see the performance difference
3. Design a BERT sentence similarity module to check if the query is similar 


Models tested - 
juierror/flan-t5-text2sql-with-schema
dawei756/text-to-sql-t5-spider-fine-tuned
gpt2
google/flan-t5-xxl