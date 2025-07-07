#These are the libraries i will work on.
import pandas as pd
from sqlalchemy import create_engine
import pyarrow as pa
import pyarrow.parquet as pq
from fastavro import writer, parse_schema
import os

#Connecting the database to python.
DB_USER = 'krish'
DB_PASSWORD = 'mysql123'
DB_HOST = 'localhost'       
DB_PORT = '3306'            
DB_NAME = 'Assignment'
TABLE_NAME = 'week_4_tasks'

#Output Files
CSV_FILE = "Week_4.csv"
PARQUET_FILE = "Week_4_Parquet.parquet"
AVRO_FILE = "Week_4_Avro.avro"


engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


df = pd.read_sql(f"Select * from {TABLE_NAME}", con=engine)

#This is the code for exporting data from MYSQL to CSV.
df.to_csv(CSV_FILE, index=false)
print("Data Exported to CSV File.")

#This is the code for exporting data from MYSQL to PARQUET.
arrow_table = pa.Table.from_pandas(df)
pq.write_table(arrow_table, PARQUET_FILE)
print("Data Exported to PARQUET File.")

#This is the code for exporting data from MYSQL to AVRO.
def generate_avro_schema(df, name="Record"):
    fields = []
    for col in df.columns:
        dtype = df[col].dtype
        if pd.api.types.is_integer_dtype(dtype):
            avro_type = "long"
        elif pd.api.types.is_float_dtype(dtype):
            avro_type = "double"
        elif pd.api.types.is_bool_dtype(dtype):
            avro_type = "boolean"
        else:
            avro_type = "string"
        fields.append({"name": col, "type": ["null", avro_type], "default": None})
    
    return {
        "doc": f"Schema for table: {TABLE_NAME}",
        "name": name,
        "namespace": "com.example",
        "type": "record",
        "fields": fields
    }

records = df.to_dict(orient='records')
schema = parse_schema(generate_avro_schema(df, name=TABLE_NAME))

with open(AVRO_FILE, 'wb') as out_file:
    writer(out_file, schema, records)

print("Data exported to AVRO_FILE")
