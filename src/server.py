from flask import Flask, jsonify, send_file, render_template
import requests
import cv2
import numpy as np
import time
import csv
import threading
from tensorflow.keras.models import load_model
from datetime import datetime
import io
import os

CAM_URL = "http://192.168.137.103/cam.jpg"  # change to the real IP of the ESP32S3
INTERVAL = 3  # seconds per capture

model = load_model('models/birdclassifier95_3.keras')
class_names = [
    'Asian-Green-Bee-Eater',
    'Coppersmith-Barbet',
    'Jungle-Babbler',
    'No Bird Detected',
    'Red-Wattled-Lapwing',
    'White-Breasted-Kingfisher'
]

last_image = None
last_prediction = "Esperando datos..."
detections = []

app = Flask(__name__, static_folder="static", template_folder="templates")

def preprocess_frame(frame):
    resized_frame = cv2.resize(frame, (256, 256))
    rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    return rgb_frame

# -- CLASIFICATION --
def predict_class(frame):
    processed = preprocess_frame(frame)
    predictions = model.predict(np.expand_dims(processed, axis=0))
    predicted_index = np.argmax(predictions)
    return class_names[predicted_index]

def capture_loop():
    global last_image, last_prediction, detections
    while True:
        try:
            response = requests.get(CAM_URL, timeout=3)
            image = cv2.imdecode(np.asarray(bytearray(response.content)), 1)
            if image is None:
                print("Error: empty image")
                time.sleep(INTERVAL)
                continue

            prediction = predict_class(image)
            last_image = image
            last_prediction = prediction

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            detections.append([timestamp, prediction])
            print(f"[{timestamp}] {prediction}")

            # Save to csv - delete if you want
            # ------------------------------------------
            if not os.path.exists('bird_detected_esp.csv'):
                with open('bird_detected_esp.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Timestamp', 'Prediction'])

            with open('bird_detected_esp.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, prediction])
            #--------------------------------------------

        except Exception as e:
            print("Error:", e)

        time.sleep(INTERVAL)

# -- API ROUTES --
@app.route("/api/latest", methods=["GET"])
def get_latest():
    """Returns the last prediction and timestamp"""
    if last_image is None:
        return jsonify({"status": "waiting for data"}), 202
    return jsonify({
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "prediction": last_prediction
    })

@app.route("/api/latest_image", methods=["GET"])
def get_latest_image():
    """Returns the last image in JPEG format"""
    global last_image
    if last_image is None:
        return jsonify({"error": "no image yet"}), 404

    _, buffer = cv2.imencode(".jpg", last_image)
    return send_file(
        io.BytesIO(buffer.tobytes()),
        mimetype='image/jpeg',
        as_attachment=False,
        download_name='latest.jpg'
    )

# -- TO RUN HTML TOO --
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    threading.Thread(target=capture_loop, daemon=True).start()

    print("Server on: http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
