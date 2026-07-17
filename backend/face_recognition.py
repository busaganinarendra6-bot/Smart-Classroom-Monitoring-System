import cv2
import os
import numpy as np
from insightface.app import FaceAnalysis

# -----------------------------
# Load InsightFace Model
# -----------------------------
app = FaceAnalysis(name="buffalo_l")

# Use CPU
app.prepare(ctx_id=-1, det_size=(640, 640))

# -----------------------------
# Known Faces
# -----------------------------
known_embeddings = []
known_names = []

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWN_FOLDER = os.path.join(BASE_DIR, "known_faces")

print("Known Faces Folder:", KNOWN_FOLDER)

# Create folder if it doesn't exist
if not os.path.exists(KNOWN_FOLDER):
    os.makedirs(KNOWN_FOLDER)
    print("Created folder:", KNOWN_FOLDER)

# Load known faces
for file in os.listdir(KNOWN_FOLDER):

    if file.lower().endswith((".jpg", ".jpeg", ".png")):

        image_path = os.path.join(KNOWN_FOLDER, file)

        image = cv2.imread(image_path)

        if image is None:
            print(f"Cannot read image: {file}")
            continue

        faces = app.get(image)

        if len(faces) == 0:
            print(f"No face detected in {file}")
            continue

        embedding = faces[0].embedding

        known_embeddings.append(embedding)

        name = os.path.splitext(file)[0]

        known_names.append(name)

        print("Loaded:", name)

print("--------------------------------")
print("Known Students:", known_names)
print("--------------------------------")


# -----------------------------
# Face Recognition
# -----------------------------
def recognize_faces(frame):

    faces = app.get(frame)

    for face in faces:

        embedding = face.embedding

        name = "Unknown"

        if len(known_embeddings) > 0:

            similarities = []

            for known_embedding in known_embeddings:

                similarity = np.dot(
                    embedding,
                    known_embedding
                ) / (
                    np.linalg.norm(embedding)
                    * np.linalg.norm(known_embedding)
                )

                similarities.append(similarity)

            best_index = np.argmax(similarities)

            if similarities[best_index] > 0.45:
                name = known_names[best_index]

        x1, y1, x2, y2 = map(int, face.bbox)

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            name,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    return frame