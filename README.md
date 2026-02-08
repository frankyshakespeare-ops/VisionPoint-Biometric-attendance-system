# VisionPoint-Biometric-attendance-system

A web-based attendance management system that uses facial recognition to automatically identify users and record their presence in real time, reducing fraud and manual errors.

## Technologies
### Backend
- Python
- Flask 

#### IA / Vision
- OpenCV 
- face_recognition 

#### Database
- SQLite 
- possible migration to PostgreSQL later

### Frontend
- HTML / CSS / JS
- Webcam with JavaScript

## Business rules
- A user must be registered before recognition
- An attendance = (user_id, date)
- Cannot clock in twice on the same day 
- The system must reject unknown faces
- Each decision must be justified (score / threshold)

## Project structure
project/
│── app.py
│── camera.py
│── face_recognition.py
│── database.py
│── models/
│   └── embeddings/
│── templates/
│── static/
│── README.md
utils/
└── config.py
