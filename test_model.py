import joblib
import pandas as pd
import numpy as np
import keras
# from sklearn.metrics import accuracy_score

def test_saved_model(type):
    dataset = pd.read_excel('dataset/'+f'{type}_dataset.xlsx')
    X = dataset.drop('Target', axis=1)
    y = dataset['Target']

    y = keras.utils.to_categorical(y)

    model = joblib.load('model/'+f'{type}_RFmodel.pkl')

    # 테스트 데이터에 대해 예측 수행
    y_pred = model.predict(X)

    y = np.argmax(y, axis=-1).tolist()
    y_pred = np.argmax(y_pred, axis=-1).tolist()

    print("True Label\n", y)
    print("\nPredicted Label\n", y_pred)

    # # 성능 지표 계산
    # test_acc = accuracy_score(y, y_pred)
    # print(f"Test accuracy: {test_acc:.5f}")


