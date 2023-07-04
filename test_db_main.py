import pandas as pd
from data_access_db import get_data_from_db
from db_data_processing import load_and_rename_column_db_data, preprocess_ultra, preprocess_sex, leave_feature_columns, concat_surgeryid, preprocess_bodypart 
import openpyxl

# # Parameters for test (김대겸씨)
# patient_id = '180000611'
# surgery_date = '20220620'

patient_id = "210038775"
surgery_date = "20230215"

# patient_id = '180006545'
# surgery_date = '20221020'


# Connect to DB server, and get data
db_access_data = get_data_from_db(patient_id, surgery_date)

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

# print(db_proessed_data)
# db_proessed_data.to_excel("./emr_scan_ultra_test.xlsx", index=False)