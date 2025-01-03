import os
import time
import logging
import cv2 as cv
from collections import deque
from PIL import Image
from twilio.rest import Client  # Twilio API
from ultralytics import YOLO
import math

MODEL_DIR = './runs/detect/train/weights/best.pt'

# Ensure the logs directory exists
os.makedirs("./logs", exist_ok=True)
os.makedirs("./detections", exist_ok=True)  # Folder to save detection clips

logging.basicConfig(
    filename="./logs/log.log", 
    filemode='a', 
    level=logging.INFO, 
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s'
)

# Twilio credentials (replace these with your actual Twilio credentials)
TWILIO_ACCOUNT_SID = 'AC73c170381bb20a1f463e1efeb379c07c'
TWILIO_AUTH_TOKEN = 'a96447c5f21842a8d3f26cce64299cc5'
TWILIO_PHONE_NUMBER = '+12184838878'
RECIPIENT_PHONE_NUMBER = '+916398549678'  # Phone number to send SMS to

# GPS coordinates for the camera location 
LATITUDE = '30.392160'
LONGITUDE = ' 79.318633'  

# Load the YOLO model
model = YOLO('best.pt')

class_names = [
    'antelope', 'bear', 'cheetah', 'human', 'coyote', 'crocodile', 'deer', 'elephant', 'flamingo',
    'fox', 'giraffe', 'gorilla', 'hedgehog', 'hippopotamus', 'hornbill', 'horse', 'hummingbird', 'hyena',
    'kangaroo', 'koala', 'leopard', 'lion', 'meerkat', 'mole', 'monkey', 'moose', 'okapi', 'orangutan',
    'ostrich', 'otter', 'panda', 'pelecaniformes', 'porcupine', 'raccoon', 'reindeer', 'rhino', 'rhinoceros',
    'snake', 'squirrel', 'swan', 'tiger', 'turkey', 'wolf', 'woodpecker', 'zebra'
]

alert_animals = ['tiger', 'elephant', 'leopard', 'deer', 'bear', 'cheetah', 'lion']  # Animals to trigger alerts

# Function to send SMS using Twilio
def send_sms(message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=RECIPIENT_PHONE_NUMBER
    )
    print(f"SMS Sent: {message.sid}")

def save_clip(buffer, fps, frame_size, timestamp):
    clip_filename = f"./detections/detection_{timestamp}.mp4"
    out = cv.VideoWriter(clip_filename, cv.VideoWriter_fourcc(*'mp4v'), fps, frame_size)
    for frame in buffer:
        out.write(frame)
    out.release()
    logging.info(f"Saved video clip: {clip_filename}")
    print(f"Saved video clip: {clip_filename}")

def main():
    print("AnimalDetection")
   

    # Mobile camera URL, replace with your camera stream URL
    mobile_camera_url = "http://192.0.0.4:8080/video"  # Replace with your IP Webcam stream URL

    # Open the camera stream
    cap = cv.VideoCapture(mobile_camera_url)

    if not cap.isOpened():
        print("Error: Could not access mobile camera.")
        return

    print("Starting live detection...")

    last_alert_time = 0  # To track last SMS sent time
    alert_interval = 30  # Interval in seconds

    fps = int(cap.get(cv.CAP_PROP_FPS))
    frame_size = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
    buffer_size = fps * 5  # 5-second buffer
    frame_buffer = deque(maxlen=buffer_size)  # To store frames for the last 5 seconds

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to retrieve frame. Check the IP camera feed URL.")
            break

        frame_buffer.append(frame)  # Add current frame to buffer

        # Perform inference with YOLO model
        results = model(frame, stream=True)

        # Process bounding boxes and display results
        for info in results:
            boxes = info.boxes
            for box in boxes:
                confidence = box.conf[0]
                confidence = math.ceil(confidence * 100)
                class_index = int(box.cls[0])

                if confidence > 80:  # Adjust the confidence threshold if needed
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    # Display bounding box and class label
                    label = f'{class_names[class_index]} {confidence}%'
                    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv.putText(frame, label, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    # Send SMS alert and save video clip if a specified animal is detected
                    current_time = time.time()
                    if class_names[class_index] in alert_animals and (current_time - last_alert_time >= alert_interval or last_alert_time == 0):
                        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
                        message = f"Animal detected at {timestamp}: {class_names[class_index]} with {confidence}% confidence. Location: Latitude {LATITUDE}, Longitude {LONGITUDE}."
                        send_sms(message)
                        logging.info(f"Sent SMS: {message}")
                        save_clip(list(frame_buffer), fps, frame_size, timestamp)
                        last_alert_time = current_time

        # Display the frame with detected objects
        cv.imshow('Animal Detection', frame)

        # Press 'q' to quit the loop
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
