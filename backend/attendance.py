import pandas as pd
from datetime import datetime
import os

FILE_NAME = "reports/attendance.csv"


def save_attendance(students, attendance, empty_seats):

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "DateTime": [now],
        "Students": [students],
        "Attendance (%)": [attendance],
        "Empty Seats": [empty_seats]
    }

    df = pd.DataFrame(data)

    if os.path.exists(FILE_NAME):

        if os.path.getsize(FILE_NAME) > 0:
            df.to_csv(FILE_NAME, mode="a", header=False, index=False)
        else:
            df.to_csv(FILE_NAME, index=False)

    else:
        df.to_csv(FILE_NAME, index=False)