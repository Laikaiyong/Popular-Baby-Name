import pandas as pd
import sqlite3

conn = sqlite3.connect("database.sqlite", isolation_level=None,
                       detect_types=sqlite3.PARSE_COLNAMES)
db_df = pd.read_sql_query("SELECT * FROM NationalNames", conn)
db_df.to_csv('database.csv', index=False)