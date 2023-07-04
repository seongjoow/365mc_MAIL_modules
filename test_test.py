from main import predict_and_return

patient_id = "210038775"
surgery_date = "20230215"

patient_id, surgery_date, predictions, confidences = predict_and_return(patient_id, surgery_date)