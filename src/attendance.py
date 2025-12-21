import csv
import os
from datetime import datetime


class AttendanceLogger:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
        self._marked = False

    def mark_once(self, name: str, roll_no: str):
        if self._marked:
            return False
        now = datetime.now().isoformat(timespec='seconds')
        exists = os.path.exists(self.csv_path)
        with open(self.csv_path, 'a', newline='') as f:
            writer = csv.writer(f)
            if not exists:
                writer.writerow(['name', 'roll_no', 'timestamp'])
            writer.writerow([name, roll_no, now])
        self._marked = True
        return True
