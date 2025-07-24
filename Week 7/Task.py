import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine

engine = create_engine("mssql+pyodbc://username:password@your_server/db_name?driver=ODBC+Driver+17+for+SQL+Server")

data_folder = 'data/raw'  
#Utility Functions
def extract_date_from_filename(name, pattern_type):
    if pattern_type == "CUST_MSTR":
        return datetime.strptime(name.split("_")[-1].split(".")[0], "%Y%m%d").date()
    elif pattern_type == "master_child_export":
        return datetime.strptime(name.split("-")[-1].split(".")[0], "%Y%m%d").date()
    return None

def truncate_table(table_name):
    with engine.connect() as conn:
        conn.execute(f"TRUNCATE TABLE {table_name}")
        print(f"{table_name} truncated.")

files = os.listdir(data_folder)

cust_mstr_files = [f for f in files if f.startswith("CUST_MSTR_")]
master_child_files = [f for f in files if f.startswith("master_child_export")]
ecom_files = [f for f in files if f.startswith("H_ECOM_ORDER")]

#Truncate all relevant tables before load
truncate_table("CUST_MSTR")
truncate_table("master_child")
truncate_table("H_ECOM_Orders")

#1.Process CUST_MSTR files
for file in cust_mstr_files:
    date_val = extract_date_from_filename(file, "CUST_MSTR")
    df = pd.read_csv(os.path.join(data_folder, file))
    df['Date'] = date_val
    df.to_sql("CUST_MSTR", engine, index=False, if_exists='append')

#2.Process master_child_export files
for file in master_child_files:
    date_val = extract_date_from_filename(file, "master_child_export")
    date_key = date_val.strftime("%Y%m%d")
    df = pd.read_csv(os.path.join(data_folder, file))
    df['Date'] = date_val
    df['DateKey'] = date_key
    df.to_sql("master_child", engine, index=False, if_exists='append')

#3.Process H_ECOM_ORDER file(s)
for file in ecom_files:
    df = pd.read_csv(os.path.join(data_folder, file))
    df.to_sql("H_ECOM_Orders", engine, index=False, if_exists='append')

print("ETL Process Completed.")
