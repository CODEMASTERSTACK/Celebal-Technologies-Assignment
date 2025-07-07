import pandas as pd
from sqlalchemy import create_engine, inspect, text


SOURCE_DB = {
    "user": "Krish",
    "password": "mysql123",
    "host": "localhost",
    "port": "3306",
    "database": "database_1"
}

DEST_DB = {
    "user": "Krish",
    "password": "mysql123",
    "host": "localhost",
    "port": "3306",
    "database": "copy_database"
}


src_engine = create_engine(f"mysql+pymysql://{SOURCE_DB['user']}:{SOURCE_DB['password']}@{SOURCE_DB['host']}:{SOURCE_DB['port']}/{SOURCE_DB['database']}")
dest_engine = create_engine(f"mysql+pymysql://{DEST_DB['user']}:{DEST_DB['password']}@{DEST_DB['host']}:{DEST_DB['port']}/{DEST_DB['database']}")

#Create Inspector
inspector = inspect(src_engine)
tables = inspector.get_table_names()

print(f"Found {len(tables)} tables in source DB: {tables}")

#Copy Each Table
for table in tables:
    print(f"\nCopying table: {table}")

    #Get CREATE TABLE statement
    with src_engine.connect() as conn:
        result = conn.execute(text(f"SHOW CREATE TABLE `{table}`")).fetchone()
        create_stmt = result[1]

    #Create table in destination
    with dest_engine.connect() as conn:
        print(f"Creating table {table} in destination DB")
        conn.execute(text(f"DROP TABLE IF EXISTS `{table}`"))  
        conn.execute(text(create_stmt))

    #Read from source
    df = pd.read_sql(f"SELECT * FROM `{table}`", con=src_engine)

    #Write to destination
    df.to_sql(table, con=dest_engine, if_exists='append', index=False)
    print(f"Data copied: {len(df)} rows")

print("\n All tables copied successfully!")
