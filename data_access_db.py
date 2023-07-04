# Module accessing to DataBase

import pandas as pd
import sqlalchemy
import pyodbc
from sqlalchemy.sql import text
from sqlalchemy import create_engine


def get_data_from_db(patient_id: str, surgery_date: str) -> pd.DataFrame:

    # DB login info
    server = '52.231.39.219' 
    database = 'tsfmc_data' 
    username = 'mc365' 
    password = 'tkadbrdhmc1!'  
    file_path = './query.txt'

    engine = create_engine("mssql+pyodbc://" + username + ":" + password + "@" + server + "/" + database + "?driver=SQL+Server")


    # Open and read query
    with open(file_path, 'r', encoding='UTF8') as file:
        sql = file.read()


    # Connect to database
    with engine.begin() as conn:
        # Create text from query
        query = text(sql)
        # Save result to dataframe
        df = pd.read_sql_query(query, conn)

    # Select surgery based on specified patient_id and date_of_discovery
    db_data = df[(df['고객번호'] == patient_id) & (df['수술일자'] == surgery_date)]
    
    # Exception
    if db_data.empty:
        # when patient_id not exist
        if db_data['고객번호'].isin([patient_id]).any():
            print(f"수술일자 {surgery_date}에 해당하는 수술이 없습니다.")

        # when surgery_date not exist
        elif db_data['수술일자'].isin([surgery_date]).any():
            print(f"고객번호 {patient_id}에 해당하는 수술이 없습니다.")

        # when both not exist
        else:
            print("해당 고객번호와 수술일자를 가진 데이터가 데이터베이스에 없습니다.")


    # Close connection
    conn.close()

    return db_data



