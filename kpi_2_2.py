import pandas as pd
import glob
import os
import numpy as np
import csv

class Kpi:
    def __init__(self, 
                 patientID: str, 
                 date: str, 
                 cam: int, 
                 section_size: int, 
                 acceptable_missing_frames: int,
                 max_section_number: int,
                 df_coord: pd.DataFrame):
        
        # customerID(str): 고객번호입니다.
        # date(str): 수술일자입니다.
        # cam(int): Cam번호입니다. 1 또는 2의 값을 갖습니다. Cam을 기준으로 프레임 정보를 갱신합니다.
        # section_size(int): 전체 수술을 등시간으로 나눌 때 구간의 길이입니다. 단위는 프레임입니다.
        # acceptable_missing_frames(int): 스트로크를 정의할 때, 두 극소점 사이 허용되는 연속 결측 프레임 개수입니다.
        # max_section_number(int): 각 수술의 길이는 상이하기 때문에, 최종 결과의 크기를 통일하기 위한 최대 구간 개수입니다.
        # folder_path(str): 수술 데이터의 최상위 폴더입니다. (ex. '36000000020230420/')

        # min_frame_number(int): 해당 Cam의 수술의 전체 영상의 최초 프레임 번호입니다. 
        # max_frame_number(int): 해당 Cam의 수술의 전체 영상의 마지막 프레임 번호입니다.
        # whole_surgery_data_path(str): 해당 전체 수술에 대한 파일 경로입니다.

        # Options
        self.patientID: str = patientID
        self.date: str = date
        self.cam: int = cam
        self.section_size: int = section_size
        self.acceptable_missing_frames: int = acceptable_missing_frames
        self.max_section_number: int = max_section_number
        self.data: pd.DataFrame = df_coord

        # Info of Data
        self.min_frame_number: int = None
        self.max_frame_number: int = None
        # self.whole_surgery_data_path: str = None

        # File Path Setting
        # self.whole_surgery_data_path = os.path.join(folder_path, 'coordinate.csv')
        
        # print(self.whole_surgery_data_path)
        self.load_data()
        self.filter_data()
        self.check_empty_result()

    def load_data(self):
        # self.data = pd.read_csv(self.whole_surgery_data_path)
        if self.data.empty:
            raise Exception('coordinate.csv에 row가 없습니다.')

    def filter_data(self):
        self.filtered_data = self.data[self.data['cam'] == self.cam]

    def check_empty_result(self):
        if self.filtered_data.empty:
            raise Exception('지정한 cam에 해당하는 row가 coordinate.csv에 없습니다.')

        
    def summary(self):
        # 수술 정보를 출력합니다.
        # 1. 고객번호
        # 2. 수술일자
        # 3. Cam번호
        # 4. 클러스터 개수
        # 5. 최대 프레임 번호
        # 6. 총 프레임 개수
        # 7. 결측 프레임 개수
        print("1. 고객번호:", self.patientID)
        print("2. 수술일자:", self.date)
        print("3. Cam번호:", self.cam)


    def cal_local_minima(self, input_df: pd.DataFrame) -> list:
        # 입력받은 데이터에서 집도의의 손의 속도의 극소점을 찾습니다.
        # 극소점의 프레임 번호를 리스트로 return
        # return되는 리스트의 len()값이 극소점의 개수입니다.
        # return ex. [30, 54, 72, ...]

        result = list()

        df = input_df
        df = df[df['cam'] == self.cam]

        # 이동거리 계산
        df['diff_x'] = df['x'].diff().fillna(0)
        df['diff_y'] = df['y'].diff().fillna(0)
        df['diff_z'] = df['z'].diff().fillna(0)
        df['distance'] = np.sqrt(df['diff_x']**2 + df['diff_y']**2 + df['diff_z']**2)

        # 누적 이동거리의 차이(point 간 이동거리)를 시간의 차이(1frame = 1/30s)로 나누어 속도(단위: m/s) 계산
        df['speed'] = df['distance'] / ((df['frame'] - df['frame'].shift())/30)
        df['speed'].fillna(0, inplace=True)

        # 속도의 차이를 시간의 차이로 나누어 가속도(단위: m/s^2) 계산
        df['acceleration'] = (df['speed'] - df['speed'].shift()) / ((df['frame'] - df['frame'].shift())/30)
        df['acceleration'].fillna(0, inplace=True)

        # 가속도가 음수에서 양수로 바뀌는 프레임 값을 리스트로 저장
        result = []
        for i in range(len(df.index)-1):
            if df['acceleration'].iloc[i] < 0 and df['acceleration'].iloc[i+1] > 0:
                result.append(df['frame'].iloc[i])

        return result

    
    def count_valid_stroke(self, local_minima_list: list, input_df: pd.DataFrame) -> int:
        # 극소점의 프레임 번호 리스트를 이용하여 유효한 스트로크 개수를 return
        # 두 극소점 사이에 존재하는 연속 결측 프레임 개수가 self.acceptable_missing_frames 미만이면
        # 해당 두 극소점을 잇는 스트로크는 유효한 스트로크로 정의합니다.
        # 모든 스트로크가 유효할 경우, 스트로크 개수는 (극소점 개수 - 1)입니다.
        # cal_local_minima() 사용
        # return ex. 1029

        if len(local_minima_list) <= 1: return 0

        unidentified_strokes = len(local_minima_list) - 1
        unvalid_stokes = 0

        df = input_df

        for i in range(len(local_minima_list)):
            if local_minima_list[i] in df['frame'].values:
                start_index = df[df['frame'] == local_minima_list[i]].index[0]
                if i < len(local_minima_list) - 1 and local_minima_list[i+1] in df['frame'].values:
                    end_index = df[df['frame'] == local_minima_list[i+1]].index[0]
                else:
                    break

                subset = df.iloc[start_index:end_index+1]

                for j in range(len(subset) - 1):
                    if (subset.iloc[j+1]['frame'] - subset.iloc[j]['frame'] - 1) <= self.acceptable_missing_frames:
                        continue
                    else:
                        unvalid_stokes += 1
                        break
                    
        return unidentified_strokes - unvalid_stokes


    # 등간 구간별 스트로크 횟수 추출 함수
    def cal_section_stroke(self, input_df: pd.DataFrame) -> list:
        # 전체 수술 데이터에 대하여 구간별 스트로크 개수를 구하고
        # 이를 리스트로 return
        # return ex. [324, 23, 2218, 0, 21, ...]
        # 주의: Cam 정보가 적용된 df를 사용함.

        df = input_df
        result = list()

        # frame번호의 최소와 최대 값을 기록
        self.min_frame_number = df['frame'].min()
        self.max_frame_number = df['frame'].max()

        # df를 self.section_size 크기의 구간으로 나누어 df_list에 저장
        df_list = []
        n = self.min_frame_number
        while n < self.max_frame_number:
            start = n
            end = n + self.section_size
            section = df[(df['frame'] >= start) & (df['frame'] < end)]
            df_list.append(section)
            n = end

        # 수술을 section으로 나눴을 때 section 개수가 max_section_number보다 작을 때 빈 section에 0으로 채워 넣어서 max_section_number 만큼 section 생성
        if len(df_list) > self.max_section_number:
            for section_df in df_list[:self.max_section_number]:
                if len(section_df) == 0:
                    result.append(0)
                    continue

                local_minima_list = self.cal_local_minima(input_df=section_df)
                number_of_strokes = self.count_valid_stroke(local_minima_list=local_minima_list, input_df=section_df)
                result.append(number_of_strokes)
        else:
            for section_df in df_list:
                if len(section_df) == 0:
                    result.append(0)
                    continue

                local_minima_list = self.cal_local_minima(input_df=section_df)
                number_of_strokes = self.count_valid_stroke(local_minima_list=local_minima_list, input_df=section_df)
                result.append(number_of_strokes)

            while len(result) < self.max_section_number:
                result.append(0)

        if sum(result)==0:
            raise Exception('coordinate.csv에 유효한 스트로크가 없습니다.')
        
        # 결과 list를 return
        return result
    

    # 등간 구간별 손의 이동거리와 평균 속력 추출 함수
    def cal_section_distance_velocity(self, input_df: pd.DataFrame) -> list:
        # 전체 수술 데이터에 대하여 구간별 손의 이동거리와 평균 속력을 구하고
        # 이를 각각 리스트로 return
        # return ex. [324, 23, 2218, 0, 21, ...], [56, 36, 108, 0, 17, ...]
        # 주의: Cam 정보가 적용된 df를 사용함.

        df = input_df
        result_distance = list()
        result_velocity = list()

        # 이동거리 계산
        df['diff_x'] = df['x'].diff().fillna(0)
        df['diff_y'] = df['y'].diff().fillna(0)
        df['diff_z'] = df['z'].diff().fillna(0)
        df['distance'] = np.sqrt(df['diff_x']**2 + df['diff_y']**2 + df['diff_z']**2)
        # 누적 이동거리 계산
        df['cumulative_distance'] = df['distance'].cumsum()

        # frame번호의 최소와 최대 값을 기록
        self.min_frame_number = df['frame'].min()
        self.max_frame_number = df['frame'].max()

        # df를 self.section_size 크기의 구간으로 나누어 df_list에 저장
        df_list = []
        n = self.min_frame_number
        while n < self.max_frame_number:
            start = n
            end = n + self.section_size
            section = df[(df['frame'] >= start) & (df['frame'] < end)]
            df_list.append(section)
            n = end
        
        # section마다 이동거리, 평균 속력을 각각 result_distance, result_velocity에 저장
        if len(df_list) > self.max_section_number:
            for section_df in df_list[:self.max_section_number]:
                if len(section_df) == 0:
                    result_distance.append(0)
                    result_velocity.append(0)
                    continue

                # 해당 section에서의 손의 총 이동거리(단위: m)와 평균 속력(m/s)을 계산
                section_distance = section_df['cumulative_distance'].iloc[-1] - section_df['cumulative_distance'].iloc[0]
                
                section_frame = section_df['frame'].iloc[-1] - section_df['frame'].iloc[0]
                if section_frame != 0:
                    section_velocity = section_distance / section_frame * 30
                else:
                    # section_frame이 0인 경우(구간에 포함되는 프레임이 없는 경우) 처리
                    section_velocity = 0

                result_distance.append(section_distance)
                result_velocity.append(section_velocity)

        # 수술을 section으로 나눴을 때 section 개수가 max_section_number보다 작을 때, 빈 section에 0으로 채워 넣어 (while문) max_section_number 만큼 section 생성
        else:
            for section_df in df_list:
                if len(section_df) == 0:
                    result_distance.append(0)
                    result_velocity.append(0)
                    continue

                # 해당 section에서의 손의 총 이동거리(단위: m)와 평균 속력(m/s)을 계산
                section_distance = section_df['cumulative_distance'].iloc[-1] - section_df['cumulative_distance'].iloc[0]
                
                section_frame = section_df['frame'].iloc[-1] - section_df['frame'].iloc[0]
                if section_frame != 0:
                    section_velocity = section_distance / section_frame * 30
                else:
                    # section_frame이 0인 경우(구간에 포함되는 프레임이 없는 경우) 처리
                    section_velocity = 0

                result_distance.append(section_distance)
                result_velocity.append(section_velocity)

            while len(result_distance) < self.max_section_number:
                result_distance.append(0)
                result_velocity.append(0)

        # 결과 list들을 return
        return result_distance, result_velocity
    

    # 등간 구간별 손의 평균 가속도 추출 함수
    def cal_section_acceleration(self, input_df: pd.DataFrame) -> list:
        
        # 전체 수술 데이터에 대하여 구간별 손의 가속도의 평균을 구하고
        # 이를 리스트로 return
        # return ex. [324, 23, 2218, 0, 21, ...]
        # 주의: Cam 정보가 적용된 df를 사용함.

        df = input_df
        result_acceleration = list()
        section_list = list()

        # 이동거리 계산
        df['diff_x'] = df['x'].diff().fillna(0)
        df['diff_y'] = df['y'].diff().fillna(0)
        df['diff_z'] = df['z'].diff().fillna(0)
        df['distance'] = np.sqrt(df['diff_x']**2 + df['diff_y']**2 + df['diff_z']**2)
        # 이동거리의 차이 계산
        # df['diff_distance'] = df['distance'].diff().fillna(0)

        # frame번호의 최소와 최대 값을 기록
        self.min_frame_number = df['frame'].min()
        self.max_frame_number = df['frame'].max()

        # df를 self.section_size 크기의 구간으로 나누어 df_list에 저장
        df_list = []
        n = self.min_frame_number
        while n < self.max_frame_number:
            start = n
            end = n + self.section_size
            section = df[(df['frame'] >= start) & (df['frame'] < end)]
            df_list.append(section)
            n = end
        
        # section마다 평균 가속도를 result_acceleration에 저장
        if len(df_list) > self.max_section_number:
            for section_df in df_list[:self.max_section_number]:
                if len(section_df) == 0:
                    result_acceleration.append(0)
                    continue

                # 해당 section에서 프레임마다 손의 속력(m/s), 가속도(m/s^2)를 계산
                # 그 후 section에서의 가속도의 평균(m/s^2)을 계산
                section_frame = section_df['frame'].iloc[-1] - section_df['frame'].iloc[0]
                section_list = section_df['distance'].values.tolist()

                if section_frame != 0:
                    # 해당 section의 속력(m/s)
                    section_list = [value / section_frame * 30 for value in section_list]
                    # 해당 section의 가속도(m/s^2)
                    section_list = [value / section_frame * 30 for value in section_list]
                    # 가속도의 평균(m/s^2)
                    section_acceleration = sum(section_list) / len(section_list)
                else:
                    section_acceleration = 0

                result_acceleration.append(section_acceleration)

        # 수술을 section으로 나눴을 때 section 개수가 max_section_number보다 작을 때, 빈 section에 0으로 채워 넣어 (while문) max_section_number 만큼 section 만든다
        else:
            for section_df in df_list:
                if len(section_df) == 0:
                    result_acceleration.append(0)
                    continue

                # 해당 section에서 프레임마다 손의 속력(m/s), 가속도(m/s^2)를 계산
                # 그 후 section에서의 가속도의 평균(m/s^2)을 계산
                section_frame = section_df['frame'].iloc[-1] - section_df['frame'].iloc[0]
                section_list = section_df['distance'].values.tolist()

                
                if section_frame != 0:
                    # 해당 section의 속력(m/s)
                    section_list = [value / section_frame * 30 for value in section_list]
                    # 해당 section의 가속도(m/s^2)
                    section_list = [value / section_frame * 30 for value in section_list]
                    # 가속도의 평균(m/s^2)
                    section_acceleration = sum(section_list) / len(section_list)
                else:
                    section_acceleration = 0

                result_acceleration.append(section_acceleration)
                
            while len(result_acceleration) < self.max_section_number:
                result_acceleration.append(0)

        # 결과 list를 return
        return result_acceleration


    # 등간 구간별 z의 표준편차 추출 함수
    def cal_section_std_z(self, input_df: pd.DataFrame) -> list:
        # 전체 수술 데이터에 대하여 구간별 z의 표준편차를 구하고
        # 이를 리스트로 return
        # return ex. [324, 23, 2218, 0, 21, ...]
        # 주의: Cam 정보가 적용된 df를 사용함.

        df = input_df
        result_std_v = list()

        # frame번호의 최소와 최대 값을 기록
        self.min_frame_number = df['frame'].min()
        self.max_frame_number = df['frame'].max()

        # df를 self.section_size 크기의 구간으로 나누어 df_list에 저장
        df_list = []
        n = self.min_frame_number
        while n < self.max_frame_number:
            start = n
            end = n + self.section_size
            section = df[(df['frame'] >= start) & (df['frame'] < end)]
            df_list.append(section)
            n = end
        
        # section마다 z의 표준편차를 result_std_v 저장
        if len(df_list) > self.max_section_number:
            for section_df in df_list[:self.max_section_number]:
                if len(section_df) <= 1: # 유효한 좌표 프레임이 2개 이상인 경우에만 해당 구간의 z 표준편차 값이 정의되므로.
                    result_std_v.append(0)
                    continue

                # 해당 section에서의 z 표준편차를 계산
                section_centroid = section_df['z'].std()
                result_std_v.append(section_centroid)

        # 수술을 section으로 나눴을 때 section 개수가 max_section_number보다 작을 때, 빈 section에 0으로 채워 넣어 (while문) max_section_number 만큼 section 생성
        else:
            for section_df in df_list:
                if len(section_df) <= 1: # 유효한 좌표 프레임이 2개 이상인 경우에만 해당 구간의 z 표준편차 값이 정의되므로.
                    result_std_v.append(0)
                    continue

                # 해당 section에서의 z 표준편차를 계산
                section_centroid = section_df['z'].std()
                result_std_v.append(section_centroid)

            while len(result_std_v) < self.max_section_number:
                result_std_v.append(0)

        # 결과 list를 return
        return result_std_v


    # 결과 딕셔너리 반환 함수
    def return_result_dict(self) -> dict():
        # 데이터를 불러와 설정한 cam에 해당하는 데이터를 사용합니다.
        # df = pd.read_csv(self.whole_surgery_data_path)
        df = self.data
        df = df[df['cam'] == self.cam]
        # x, y, z 좌표 중 하나라도 NaN인 프레임은 drop하여 사용합니다.
        df.dropna(subset=['x', 'y', 'z'], inplace=True)

        # 구간별 KPI 특징점을 계산합니다.
        section_num_stroke = self.cal_section_stroke(input_df=df)
        section_dist, section_vel = self.cal_section_distance_velocity(input_df=df)
        section_acc = self.cal_section_acceleration(input_df = df)
        section_std_z = self.cal_section_std_z(input_df = df)

        # 반환할 dict를 생성합니다.
        result = dict()

        # 결과 dict에 환자번호, 수술일자 정보를 입력합니다.
        result['PatientID'] = self.patientID
        result['SurgeryDate'] = self.date

        # 결과 dict에 계산된 KPI 특징점을 입력합니다.

        # 등간 구간 길이 (min)
        result['SectionSize(m)'] = self.section_size / 1800

        # 등간 구간별 스트로크 횟수 (편도)
        for i in range(1, self.max_section_number+1):
            result['NumOfStrokes_section'+str(i)] = section_num_stroke[i-1]

        # 등간 구간별 손의 이동거리 (m)
        for i in range(1, self.max_section_number+1):
            result['CumDistOfStrokes_section'+str(i)] = section_dist[i-1]

        # 등간 구간별 손의 평균 속력 (m/s)
        for i in range(1, self.max_section_number+1):
            result['AvgVelOfStrokes_section'+str(i)] = section_vel[i-1]

        # 등간 구간별 손의 가속도의 평균 (m/s^2)
        for i in range(1, self.max_section_number+1):
            result['AvgAccOfStrokes_section'+str(i)] = section_acc[i-1]

        # 등간 구간별 z좌표 표준편차
        for i in range(1, self.max_section_number+1):
            result['StdOfZ_section'+str(i)] = section_std_z[i-1]
        
        
        # 결과 dict를 return
        return result
    

    # Result Example
    # {
    #     "customerID" : '123456789',
    #     "date": '20230420',
    #     "NumberOfStrokes_section1": 30,
    #     "NumberOfStrokes_section2": 130,
    #     ...
    # }
