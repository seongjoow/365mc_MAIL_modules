import pandas as pd
from data_access_db import get_data_from_db
from db_data_processing import load_and_rename_column_db_data, preprocessing_ultra, preprocessing_sex, only_feature_columns, concat_surgeryid, preprocessing_bodypart 
import openpyxl

# Parameters for test
patient_id = '180000611'
date_of_surgery = '20220620'

start = get_data_from_db('180000611', '20220620')
print(start)

start2 = load_and_rename_column_db_data('180000611', '20220620')
print(start2)

ultra = preprocessing_ultra(start2)
print(ultra)

sex = preprocessing_sex(ultra)
print(sex)

feature = only_feature_columns(ultra)
print(feature)

surgeryid = concat_surgeryid(feature)
print(surgeryid)

result = preprocessing_bodypart(surgeryid)
print(result)

result.to_excel("./결과물테스트.xlsx", index=False)