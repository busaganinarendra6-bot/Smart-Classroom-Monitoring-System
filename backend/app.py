from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import cv2

from backend.detector import count_students, detect_students
from backend.attendance import save_attendance
from backend.face_recognition import recognize_faces

app = FastAPI()

# -----------------------------
# Serve Frontend Files
# -----------------------------
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# -----------------------------
# Enable CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# LOGIN PAGE
# =====================================================

@app.get("/")
def login():
    return FileResponse("frontend/login.html")


@app.get("/login")
def login_page():
    return FileResponse("frontend/login.html")

@app.get("/register")
def register():
    return FileResponse("frontend/register.html")


# =====================================================
# DASHBOARD
# =====================================================

@app.get("/dashboard")
def dashboard():
    return FileResponse("frontend/index.html")


# =====================================================
# STUDENT COUNT API
# =====================================================

@app.get("/student-count")
def student_count():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return {"error": "Camera not found"}

    success, frame = cap.read()

    cap.release()

    if not success:
        return {"error": "Cannot read camera"}

    # Detect Students
    count = count_students(frame)

    TOTAL_STUDENTS = 30

    attendance = round((count / TOTAL_STUDENTS) * 100, 1)

    empty_seats = TOTAL_STUDENTS - count

    # Save Attendance
    save_attendance(
        count,
        attendance,
        empty_seats
    )

    # Classroom Status
    if count == 0:
        status = "🚨 Classroom Empty"
    elif attendance < 50:
        status = "⚠ Low Attendance"
    else:
        status = "✅ Normal"

    return {
        "students": count,
        "attendance": attendance,
        "empty_seats": empty_seats,
        "status": status
    }


# =====================================================
# CAMERA STREAM
# =====================================================

def generate_frames():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return

    while True:

        success, frame = cap.read()

        if not success:
            break

        try:
            # Student Detection
            frame, count = detect_students(frame)

            # Face Recognition
            frame = recognize_faces(frame)

        except Exception as e:
            print("Detection Error:", e)

        ret, buffer = cv2.imencode(".jpg", frame)

        if not ret:
            continue

        frame_bytes = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame_bytes +
            b'\r\n'
        )

    cap.release()


# =====================================================
# VIDEO STREAM API
# =====================================================

@app.get("/video")
def video():

    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )