import pandas as pd
from sqlalchemy import create_engine, text

SOURCE_DB_URI = "mysql+pymysql://user:password@localhost:3306/source_db"
DEST_DB_URI   = "mysql+pymysql://user:password@localhost:3306/destination_db"

#Copying the specific columns
tables_to_copy = {
    "students": ["id", "name"],              
    "teachers": ["id", "subject"],           
    "courses": ["course_id", "course_name"]  
}

src_engine = create_engine(SOURCE_DB_URI)
dest_engine = create_engine(DEST_DB_URI)

#Copy Data for Each Table
for table, columns in tables_to_copy.items():
    print(f"Copying {columns} from {table}")

    cols_str = ", ".join(columns)

    # Read from source
    df = pd.read_sql(f"SELECT {cols_str} FROM {table}", con=src_engine)

    #Create destination table (if needed) and write data
    df.to_sql(table, con=dest_engine, if_exists="replace", index=False)
    print(f"Done: {len(df)} rows in {table}")
