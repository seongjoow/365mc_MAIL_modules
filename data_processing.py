# Module for join and processing data

import pandas as pd
from data_access_db import get_data_from_db
from data_access_nas import get_data_from_nas
from db_data_processing import load_and_rename_column_db_data, preprocess_ultra, preprocess_sex, leave_feature_columns, concat_surgeryid, preprocess_bodypart 


def process_db_data(patient_id:str, date_of_surgery:str) -> pd.DataFrame:

    # Connect to DB server, and get data
    db_access_data = get_data_from_db(patient_id, date_of_surgery)

    # Load and renam the data
    renamed_data = load_and_rename_column_db_data(patient_id, date_of_surgery)

    # Add ultra column
    ultra = preprocess_ultra(renamed_data)

    # Process sex column
    sex = preprocess_sex(ultra)

    # Extract leave needed columns
    feature = leave_feature_columns(ultra)

    # Add SurgeryID column for meta_data
    surgeryid = concat_surgeryid(feature)

    # Final processed DB data
    db_proessed_data = preprocess_bodypart(surgeryid)


    return db_proessed_data


def join_and_process_data(patient_id:str, date_of_surgery:str) -> pd.DataFrame:

    # Get data from NAS
    nas_data = get_data_from_nas(patient_id, date_of_surgery)
    # Get processed_db data
    db_data = process_db_data(patient_id, date_of_surgery)

    # Check for join KPI and DB data
    db_data_flag = 0

    # Save 1 if db_data loaded successfully
    if not db_data.empty:
        db_data_flag = 1
    
    if(db_data_flag == 0):
        print(f"DB에 해당 수술 데이터가 존재하지 않아 KPI와 조인을 할 수 없습니다. 고객번호:{patient_id}, 수술날짜: {date_of_surgery}")
    
    else:
        print("KPI와 성공적으로 조인하였습니다")
        
    

    # 필터링

    # kpi generator 


    
    # Join KPI and DB data(EMR_SCAN_ULTRA)
    combined_data = pd.merge(nas_data, db_data, on='SurgeryID')  

    # Process (결측치를 채우거나, 데이터를 스케일링하거나, 특성을 추출하는 등의 작업)
    processed_data = combined_data  # 실제 처리를 위한 코드



    return processed_data
