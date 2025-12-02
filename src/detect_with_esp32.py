import cv2
import numpy as np
import time
import csv
import requests
from tensorflow.keras.models import load_model

model = load_model('models/birdclassifier95_1.keras')

detections = []
start_time = time.time()

def preprocess_frame(frame):
    resized_frame = cv2.resize(frame, (256, 256))
    # Convert frame to RGB
    rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    # Normalize pixel values
    normalized_frame = rgb_frame
    return normalized_frame

def predict_class(frame):
    processed_frame = preprocess_frame(frame)
    # Make predictions
    predictions = model.predict(np.expand_dims(processed_frame, axis=0))
    predicted_class_index = np.argmax(predictions)
    return predicted_class_index

def save_to_csv(detections):
    with open('bird_detected_esp.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Detected Bird'])
        for detection in detections:
            writer.writerow(detection)

url = 'http://http://192.168.101.14//cam.jpg'

while True:
    try:
        response = requests.get(url)
        image = cv2.imdecode(np.asarray(bytearray(response.content)), 1)

        predicted_class_index = predict_class(image)
        class_names =['Asian-Green-Bee-Eater','Coppersmith-Barbet','Jungle-Babbler','No Bird Detected','Rose Ringed Parakeet','White-Breasted-Kingfisher']
        predicted_class = class_names[predicted_class_index]

        cv2.putText(image, predicted_class, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Bird Image', image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        
        current_time = time.time()
        if current_time - start_time >= 2.5:
            detections.append([time.strftime('%Y-%m-%d %H:%M:%S'), predicted_class])
            start_time = time.time()

    except Exception as e: 
        print(f"Error: {e}")
        break

if detections:
    save_to_csv(detections)

cv2.destroyAllWindows()
