# Module for join and processing data

import pandas as pd
from kpi_generator import generate_kpi
from db_data_processing import load_and_rename_column_db_data, preprocess_ultra, preprocess_sex, leave_feature_columns, concat_surgeryid, preprocess_bodypart 


def process_db_data(patient_id:str, surgery_date:str) -> pd.DataFrame:

    # Load and renam the data
    renamed_data = load_and_rename_column_db_data(patient_id, surgery_date)

    # Add ultra column
    ultra = preprocess_ultra(renamed_data)

    # Process sex column
    sex = preprocess_sex(ultra)

    # Extract leave needed columns
    feature = leave_feature_columns(sex)

    # Add SurgeryID column for meta_data
    surgeryid = concat_surgeryid(feature)

    # Final processed DB data
    db_proessed_data = preprocess_bodypart(surgeryid)


    return db_proessed_data


def join_and_process_data(patient_id: str, surgery_date: str) -> pd.DataFrame:
    surgery_id = patient_id + surgery_date

    # Get processed_db data
    df_emr_scan_ultra = process_db_data(patient_id, surgery_date)
    df_kpi = generate_kpi(surgery_id)


    # Check for join KPI and DB data
    df_emr_scan_ultra_flag = 0
    df_kpi_flag = 0

    # Save 1 if df_emr_scan_ultra loaded successfully
    if not df_emr_scan_ultra.empty:
        df_emr_scan_ultra_flag = 1
    
    # Save 1 if df_kpi loaded successfully
    if not df_kpi.empty:
        df_kpi_flag = 1

    
    if(df_emr_scan_ultra_flag == 0):
        print(f"DB에 해당 수술 데이터가 존재하지 않아 KPI와 조인을 할 수 없습니다. 고객번호:{patient_id}, 수술날짜:{surgery_date}")
    
    elif(df_kpi_flag == 0):
        print(f"해당 수술의 KPI 객체가 생성되지 않아 EMR_SCAN_ULTRA 데이터와 조인을 할 수 없습니다. 고객번호:{patient_id}, 수술날짜:{surgery_date}")
    
    else:
        # Add 'SugeryID' column to the front
        df_kpi = concat_surgeryid(df_kpi)

        # Join KPI and EMR_SCAN_ULTRA
        merge_columns = ['SurgeryID', 'PatientID', 'SurgeryDate']
        combined_data = pd.merge(df_kpi, df_emr_scan_ultra, how='left', on = merge_columns)

        # fill Nan with zero
        combined_data = combined_data.fillna(0)
        

    processed_data = combined_data

    return processed_data
