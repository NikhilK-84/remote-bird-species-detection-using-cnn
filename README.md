# Bird Species Detection

## Overview
This project aims to detect bird species using a Convolutional Neural Network (CNN). The model was trained on six categories, including five bird species and one category for 'no bird detected'. The project includes resources for training the model and using it for detection with two different implementations:
1. Using a webcam as a source: This implementation is suitable for testing the model in a controlled environment.
2. Using an ESP32 camera as a source: The ESP32 camera can be integrated with a Raspberry Pi (or a computer) to enable remote bird detection using its WiFi functionality.

## Project Structure
bird-species-detection/<br>
│<br>
├── model_training/<br>
│   ├── train/ (to be downloaded from kaggle, link below)<br>
│   ├── test/ (to be downloaded from kaggle, link below)<br>
│   ├── val/ (to be downloaded from kaggle, link below)<br>
│   ├── train_model.ipynb<br>
│<br>
├── esp32_cam-setup/<br>
│   ├── esp-cam-setup.ino/<br>
│<br>
├── src/<br>
│   ├── models/<br>
│   │   ├── birdclassifier95.keras (to be downloaded, see instructions below)<br>
│   ├── bird_detected_webcam.csv<br>
│   ├── bird_detected_esp.csv<br>
│   ├── detect_with_webcam.py<br>
│   ├── detect_with_esp32.py<br>
|   ├── server.py<br>
|   ├── templates<br>
|   |   ├── index.html<br>
│<br>
├── README.md<br>
├── LICENSE<br>

## Instructions

## Required Softwares
* Code editor for Python (to execute Jupyter Notebooks and python scripts)
* Arduino IDE (needed for ESP32 setup)

### Library Requirements

* Python 3.x
* TensorFlow
* OpenCV
* Numpy
* Time
* CSV
* Requests
* Matplotlib
* Scikit Learn
* OS
* Libraries for ESP32 Cam:
    * http://arduino.esp8266.com/stable/package_esp8266com_index.json
    * https://dl.espressif.com/dl/package_esp32_index.json 
* To run server.py you will need to:
    * pip install flask tensorflow opencv-python requests
    * If you already have some libraries pip will not install them.

### Dataset
1. Download the dataset from Kaggle: [Kaggle Dataset Link](https://www.kaggle.com/datasets/ichhadhari/indian-birds)
2. Place the downloaded images into the respective folders (`train`, `test`, `val`) inside the `model_training` directory. This allows you to run the Jupyter notebook with the dataset.

### Model Training
* Open the `train_model.ipynb` notebook in the `model_training` directory.
* Ensure the dataset is properly placed as described above.
* Run the notebook to train the CNN model.

### Pre-trained Model
To use the pre-trained model:
1. Download the pre-trained model from Google Drive: [Download birdclassifier95.keras](https://drive.google.com/drive/folders/1w_qjfUGJaqZOIcuMml_xZSaMRJ4kt5TX?usp=sharing)
2. Place the downloaded model file in the `models` folder inside the `src` directory.

### Usage

#### Webcam Implementation
* Ensure you have the required dependencies installed.
* Navigate to the `src` directory.
* Run the following command:
    ```bash
    python detect_with_webcam.py
    ```

#### ESP32 Implementation
* Setup the ESP32 cam module (using 'esp32_cam-setup' directory and Arduino IDE)
* Ensure the libraries for esp32 are imported to IDE
* Modify the Wi-fi credentials in 'esp-cam-setup.ino' file as needed
* Upload 'esp-cam-setup.ino' to esp32 cam from computer
* Once the connection with wifi is sucessful, get the link for esp32 cam stream from serial monitor
* Modify the link (line 35 in the python script 'detect_with_esp32.py' : url = 'http://192.168.17.149/cam-mid.jpg')
* Navigate to the `src` directory.
* Run the following command:
    ```bash
    python detect_with_esp32.py
    ```

## Resources and Acknowledgements
* Dataset: [Kaggle Dataset](https://www.kaggle.com/datasets/ichhadhari/indian-birds)
* CNN Model Training: [Youtube](https://www.youtube.com/watch?v=jztwpsIzEGc)
* ESP32 Cam Setup: [Youtube](https://www.youtube.com/watch?v=A1SPJSVra9I&t=305s) 

### Update to use with XIAO ESP32S3 board
* Paste the code in xiao_esp32s3_setup/xiao-esp32s3-setup.ino into Arduino IDE, select the board XIAO_ESP32S3 and change the PSRAM option to "OPI PSRAM" to load the program into the board.
* Files server.py is meant to read the image served on the IP that the XIAO ESP32S3 sends, make the prediction and create two endpoints to load the image and the prediction in an index.html (templates/index.html). 
* It is still possible to use the "ESP32 Implementation" but use xiao-esp32s3-setup.ino instead.

## Models already trained
* the files in model-training/models and src/models are models already trainded, the file "birdclassifier95_3.keras" is trained with 500 images from the same Dataset, for val and test I used 100 images each. 