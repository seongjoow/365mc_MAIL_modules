# NAS 데이터 접근 모듈 (윈도우 용)

import paramiko
import os
import tempfile
import pandas as pd

# 원하는 수술번호 폴더에서 미터 좌표 파일 coordinate.csv를 불러옵니다.
def load_csv_from_target_dir(sftp, target_dir_name, base_dir="/data"):
    target_dir_path = base_dir+"/"+target_dir_name

    try:
        # Check if the target directory exists
        if target_dir_name in sftp.listdir(base_dir):
            csv_path = target_dir_path + "/coordinate.csv"

            try:
                sftp.stat(csv_path)
            except IOError:
                print(f"coordinate.csv 파일을 찾을 수 없습니다: {csv_path}")
                return
            
            # Create a temporary file and immediately close it
            tmpfile = tempfile.NamedTemporaryFile()
            temp_file_name = tmpfile.name
            tmpfile.close()
                
            try:
                # Download the file to the temporary file
                sftp.get(csv_path, temp_file_name)
                
                # Load temporary file into a pandas DataFrame
                df = pd.read_csv(temp_file_name)

                return df
        
            except Exception as e:
                print(f"오류가 발생했습니다: {e}")
                return
            
            finally:
                # Remove the temporary file
                if os.path.exists(temp_file_name):
                    os.unlink(temp_file_name)
                    
    except IOError:
        print(f"해당 수술 디렉토리를 찾을 수 없습니다: {target_dir_path}")


def get_data_from_nas(surgery_id: str) -> pd.DataFrame:
    target_dir_name = surgery_id

    # connect to NAS server
    transport = paramiko.Transport(('mc365.asuscomm.com', 63122))
    transport.connect(username='mc365', password='tkadbrdhMC1!')

    # open the SFTP session
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Load CSV from the target directory
    df = load_csv_from_target_dir(sftp, target_dir_name)

    # close the SFTP session
    sftp.close()
    transport.close()

    return df