# Preprocessing data from DataBase

import pandas as pd
from data_access_db import get_data_from_db



def load_and_rename_column_db_data(patient_id:str, date_of_surgery:str) -> pd.DataFrame:
   
    df = get_data_from_db(patient_id, date_of_surgery)

    if (len(df) != 0):
        print(f"성공적으로 {patient_id}고객의 {date_of_surgery}수술을 DB에서 추출하였습니다.")
    else:
        print(f"{patient_id}고객의 {date_of_surgery}수술을 DB에서 추출하는데 실패하였습니다.")

    # Rename column by meta-data
    df.rename(columns={'고객번호': 'PatientID', '수술일자': 'SurgeryDate', '부위명': 'BodyPart'}, inplace=True)

    return df


def preprocessing_ultra(input_df:pd.DataFrame) -> pd.DataFrame:

    # Add ultra size columns
    input_df['초음파사이즈1'] = 0
    input_df['초음파사이즈2'] = 0

    # Match columns with 'BodyPart'
    for i, row in input_df.iterrows():
        if row['BodyPart'] == '복부':
            input_df.at[i, '초음파사이즈1'] = row['윗배']
            input_df.at[i, '초음파사이즈2'] = row['아랫배']
        elif row['BodyPart'] == '팔':
            input_df.at[i, '초음파사이즈1'] = row['좌팔외측']
            input_df.at[i, '초음파사이즈2'] = row['좌팔내측']
        elif row['BodyPart'] == '허벅지':
            input_df.at[i, '초음파사이즈1'] = row['허뒤좌안쪽']
            input_df.at[i, '초음파사이즈2'] = row['허뒤좌외측']
        elif row['BodyPart'] == '러브핸들':
            input_df.at[i, '초음파사이즈1'] = row['좌러브']
        elif row['BodyPart'] == '등':
            input_df.at[i, '초음파사이즈1'] = row['좌브라']
        elif row['BodyPart'] == '종아리':
            input_df.at[i, '초음파사이즈1'] = row['종좌']
            input_df.at[i, '초음파사이즈2'] = row['종좌외측']

    df = input_df.drop(columns=['윗배', '아랫배', '좌팔외측', '좌팔내측', '허뒤좌안쪽', '허뒤좌외측', '좌러브', '좌브라', '종좌', '종좌외측'])

    return df


def preprocessing_sex(input_df:pd.DataFrame) -> pd.DataFrame:

    # one-hot encoding 
    input_df['성별__M'] = 0
    input_df['성별__F'] = 0
    input_df['성별__E'] = 0

    input_df.loc[input_df['성별'] == 'M', '성별__M'] = 1
    input_df.loc[input_df['성별'] == 'F', '성별__F'] = 1
    input_df.loc[~input_df['성별'].isin(['M', 'F']), '성별__E'] = 1
    input_df.loc[input_df['성별'].isna(), '성별__E'] = 1

    df = input_df.drop(['성별'], axis=1)

    return df


def only_feature_columns(input_df:pd.DataFrame) -> pd.DataFrame:

    meta_columns = ['PatientID', 'SurgeryDate', 'BodyPart']
    EMR_columns = ['기수', '수술소요시간', '나이', '흡연', '음주', '체수분', '단백질', '체중', '지방량', '체지방', '체지방량', '골격근지방골격근량', '비만진단BMI', '비만진단체지방률', '비만진단복부지방률', '기초대사량', '성별__E','성별__F', '성별__M']
    SCAN_columns = ['허벅지부분체적', '종아리우부분체적', '상복부최대둘레', '엉덩이둘레', '배꼽점둘레', '종아리부분체적', '가슴부분체적', '하복부최대둘레높이의단면적', '상복부최대둘레높이', '종아리둘레', '복부최대둘레높이', '허벅지신장비율ThightoHeightRatio', '총표면적', '복부부분체적', '명치부분체적', '허리둘레', '복부최대둘레', '하복부최대둘레', '허리엉덩이비율WaisttoHipRatio', '하복부둘레', '상복부최대둘레높이의단면적', '허리가슴비율WaisttoChestRatio', '하복부부분체적', '상복부부분체적', '골반부분체적', '종아리좌부분체적', '체질량지수', '팔둘레', '체적', '팔좌부분체적', '메쉬신장', '허벅지둘레', '허리신장비율WaisttoHeightRatio', '복부최대둘레높이의단면적', '팔우부분체적', '무릎둘레오른쪽', '가슴둘레']
    ULTRA_columns = ['초음파사이즈1', '초음파사이즈2']
    sort_column = ['측정일자_인바디']

    df = input_df[meta_columns + EMR_columns + SCAN_columns + ULTRA_columns + sort_column]

    return df


def concat_surgeryid(input_df:pd.DataFrame) -> pd.DataFrame:
    
    # create 'SurgeryID'
    input_df['SurgeryID'] = input_df['PatientID'].astype(str) + input_df['SurgeryDate'].astype(str)

    columns = input_df.columns.tolist()

    # move 'SurgeryID' column to the front
    columns = [columns[-1]] + columns[:-1]

    df = input_df[columns]

    return df


# Extract only one record
def preprocessing_bodypart(input_df:pd.DataFrame)-> pd.DataFrame:
    
    # Name of columns that has all Nan values
    nan_columns = []

    # Iterate over each column in the input dataframe
    for column in input_df.columns:

    # Check if all values in the column are NaN
        if all(input_df[column].isna()):
            
            # If all values are NaN, add the column to the nan_columns list
            nan_columns.append(column)

    # Get the columns to compare by taking the difference between all columns and nan_columns
    columns_to_compare = input_df.columns.difference(nan_columns).tolist()

    # Name the left over columns
    valid_columns = []


    for column in columns_to_compare:
        
        # Check if the values in the column are not all NaN and if there are any non-matching values
        if not all(input_df[column].notna() & (input_df[column] == input_df.iloc[0][column])):
            # If there are non-matching values, add the column to the valid_columns list
            valid_columns.append(column)


    # If 'BodyPart' are two or more including Nan, Leave only records with valid fat values.
    valid_data = input_df[input_df['지방량'].notnull()]
    valid_data

    # Select the records with the lowest nan value.
    df = valid_data[valid_data.isnull().sum(axis=1) == valid_data.isnull().sum(axis=1).min()]

    # if Nan value are two or more, select the recentest one.
    if (len(df) > 1) :
        df = df.sort_values('측정일자_인바디', ascending=False).head(1)

    df = df.drop(['측정일자_인바디'], axis = 1)

    # fill Nan to zero
    df.fillna(0, inplace=True)

    return df

