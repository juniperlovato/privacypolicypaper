# extract the data we need from the sqlite database.

import sqlite3
import os
import pandas as pd

# import privacy policy over time dataset
# this pulls in the SQL database and converts specific tables to csv

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
rel_path = "../data/release_db.sqlite"
abs_file_path = os.path.join(script_dir, rel_path)

conn = sqlite3.connect(abs_file_path)


'''
start with some basic inspection
'''

# get the number of nan values in the policy_text column of the policy_texts table
count_nans = pd.read_sql_query("SELECT COUNT(*) FROM policy_texts WHERE policy_text IS NULL", conn)
print(f"Number of rows with NaNs in policy_texts table: {count_nans.iloc[0,0]}")

# get the number of rows of the policy_texts table
count_rows = pd.read_sql_query("SELECT COUNT(*) FROM policy_texts", conn)
print(f"Total number of rows in policy_texts table: {count_rows.iloc[0,0]}")

# get the number of unique values in the policy_text_id column of the policy_snapshots table
count_unique = pd.read_sql_query("SELECT COUNT(DISTINCT policy_text_id) FROM policy_snapshots", conn)
print(f"Number of unique values in policy_text_id column of policy_snapshots table: {count_unique.iloc[0,0]}")

'''
exports
'''

# # export the policy_texts table to csv
policy_texts = pd.read_sql_query("SELECT * FROM policy_texts", conn)
policy_texts.to_csv(os.path.join(script_dir, '../data/policy_texts.csv'), index=False)

# # export the policy_snapshots table to csv
policy_snapshots = pd.read_sql_query("SELECT * FROM policy_snapshots", conn)
policy_snapshots.to_csv(os.path.join(script_dir, '../data/policy_snapshots.csv'), index=False)

# # load the sites and alexa_ranks tables into dataframes
sites = pd.read_sql_query("SELECT * FROM sites", conn)
sites.to_csv(os.path.join(script_dir, '../data/sites.csv'), index=False)

alexa_ranks = pd.read_sql_query("SELECT * FROM alexa_ranks", conn)
alexa_ranks.to_csv(os.path.join(script_dir, '../data/alexa_ranks.csv'), index=False)

# close the connection
conn.close()


