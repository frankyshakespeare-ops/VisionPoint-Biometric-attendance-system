from flask import Flask, jsonify
from camera import Camera
from face_recognition import FaceRecognitionEngine
from database import init_db, add_attendance
from datetime import datetime
from database import add_user
import sqlite3
import os


app = Flask(__name__)

# Initialisation
init_db()
camera = Camera()
engine = FaceRecognitionEngine()

# --- Routes Web ---
@app.route("/")
def index():
    return "Facial Attendance System is running"


# --- Routes API ---
@app.route("/scan", methods=["GET"])
def scan():
    frame = camera.capture_frame()

    if frame is None:
        return jsonify({
            "status": "error",
            "message": "Impossible de capturer l'image"
        }), 500

    recognized, user_id, distance = engine.recognize(frame)

    if not recognized:
        return jsonify({
            "status": "rejected",
            "message": "Visage non reconnu",
            "distance": distance
        }), 403

    success = add_attendance(user_id, distance)

    if success:
        return jsonify({
            "status": "success",
            "message": "Présence enregistrée",
            "user_id": user_id,
            "distance": distance,
            "time": datetime.now().isoformat()
        })

    return jsonify({
        "status": "duplicate",
        "message": "Présence déjà enregistrée aujourd'hui",
        "user_id": user_id
    }), 409

# Route pour enregistrer un nouvel utilisateur
@app.route("/register/<name>")
def register(name):
    frame = camera.capture_frame()

    if frame is None:
        return jsonify({
            "status": "error",
            "message": "Impossible de capturer l'image"
        }), 500

    # 1. Ajouter l'utilisateur en DB
    add_user(name)

    # 2. Récupérer l'ID du dernier utilisateur
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1")
    user_id = cursor.fetchone()[0]
    conn.close()

    # 3. Enregistrer le visage de référence
    success = engine.register_user(user_id, frame)

    if not success:
        return jsonify({
            "status": "error",
            "message": "Visage non détecté. Réessaie."
        }), 400

    return jsonify({
        "status": "success",
        "message": "Utilisateur enregistré",
        "user_id": user_id
    })



if __name__ == "__main__":
    app.run(debug=True)
