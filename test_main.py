from data_access_nas import get_data_from_nas

patient_id = "210007811"
date = "20221109"

df = get_data_from_nas(patient_id, date)

df.to_csv('coord_test.csv', index=False)