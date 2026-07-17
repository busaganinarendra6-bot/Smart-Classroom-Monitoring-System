from ultralytics import YOLO
import cv2

# Load YOLO model once
model = YOLO("yolov8n.pt")


def detect_students(frame):

    results = model(frame)

    count = 0

    for result in results:

        for box in result.boxes:

            cls = int(box.cls[0])

            if model.names[cls] == "person":

                count += 1

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                confidence = float(box.conf[0])

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                cv2.putText(
                    frame,
                    f"Person {confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

    cv2.putText(
        frame,
        f"Students: {count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        3
    )

    return frame, count


def count_students(frame):

    results = model(frame)

    count = 0

    for result in results:

        for box in result.boxes:

            cls = int(box.cls[0])

            if model.names[cls] == "person":
                count += 1

    return count