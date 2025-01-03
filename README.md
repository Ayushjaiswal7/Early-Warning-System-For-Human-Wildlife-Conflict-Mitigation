# Early-Warning-System-For-Human-Wildlife-Conflict-Mitigation
**Objective**
The primary goal of this project is to develop an intelligent, real-time early warning system to mitigate human-wildlife conflicts. The system uses advanced computer vision techniques, AI/ML models, and IoT integration to detect and classify wildlife in real-time and send timely alerts to concerned authorities or individuals.

**Overview**
Human-wildlife conflicts have increased due to habitat encroachment and urbanization, leading to risks for both humans and animals. This system aims to address these challenges by identifying potentially dangerous wildlife in monitored areas and providing immediate notifications. It can be deployed in regions prone to such conflicts, such as farmlands, wildlife reserves, or forest peripheries.

**Key Features**
Real-Time Detection:
->Utilizes YOLO (You Only Look Once) object detection models for fast and accurate identification of animals.
->Detects and classifies species based on live video feeds from IP cameras, Raspberry Pi cameras, or mobile devices.

**Raspberry Pi Integration:**
The system is designed to interface with Raspberry Pi devices and their connected cameras.
Enables installation in remote and forested areas where human-wildlife conflict is prevalent.
The compact, low-power Raspberry Pi setup is ideal for continuous monitoring in remote locations.

**Alert Mechanism:**
Sends SMS alerts to designated recipients (e.g., local wildlife authorities or farmers) via Twilio API when specific high-risk animals are detected.
Includes the detection timestamp, animal classification, confidence score, and GPS coordinates.

**Video Capture and Upload:**
Automatically saves a 5-second video clip of detections for verification.
Uploads the video clip to Google Drive and includes the download link in the SMS alert for instant access.

Configurable Animal Alert List:

Users can define specific animals (e.g., tiger, elephant, leopard) that trigger alerts.
Ensures the system focuses on species most relevant to the location.
Scalability:

Capable of integrating with multiple cameras across large areas.
Expandable to detect a wider range of species or integrate with IoT-based deterrents like alarms or lights.
Technologies Used
AI and Machine Learning:

YOLO model for real-time object detection.
Python for implementation and automation.
APIs:

Twilio for SMS alerts.
Google Drive API for secure video storage and sharing.

**Hardware:**
Raspberry Pi as the central processing unit in remote locations.
Raspberry Pi Camera for live video feed capture.
IP Cameras for flexible monitoring options.

Libraries:
OpenCV for video capture and processing.
PIL for image handling.
Math and Logging for calculations and diagnostics.

**Workflow**
->Input:
  Real-time video feed from an IP camera or Raspberry Pi Camera.
->Processing:
  YOLO model detects animals and classifies them by species.
  Confidence thresholds filter out false positives.
->Output:
  Alerts sent via SMS for critical species detections.
  A video clip is saved locally and uploaded to Google Drive.
  The SMS includes a link to the video and the detection details.

**Applications**
Remote Forest Surveillance: Monitoring wildlife in human-conflict-prone forest areas using Raspberry Pi for low-cost, efficient deployments.
Wildlife conservation efforts to monitor and protect endangered species.
Conflict mitigation in rural and urban areas prone to human-wildlife interactions.
Agricultural protection by warning farmers of approaching wildlife.
Enhancing safety for trekking routes or eco-tourism locations.







