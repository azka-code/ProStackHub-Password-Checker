import time
import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from database import save_event, init_database


LOG_FILE = "logs/security.log"


class LogHandler(FileSystemEventHandler):

    def __init__(self):

        if os.path.exists(LOG_FILE):
            self.last_position = os.path.getsize(LOG_FILE)
        else:
            self.last_position = 0

    def on_modified(self, event):

        if not event.src_path.endswith("security.log"):
            return

        try:

            with open(LOG_FILE, "r") as file:

                file.seek(self.last_position)

                new_lines = file.readlines()

                self.last_position = file.tell()

            for line in new_lines:

                line = line.strip()

                if not line:
                    continue

                parts = line.split("|", 3)

                if len(parts) == 4:

                    timestamp, event_type, severity, message = parts

                    save_event(
                        event_type,
                        severity,
                        message
                    )

                    print(
                        f"[ALERT] {event_type} | {severity}"
                    )

        except Exception as error:

            print("[ERROR]", error)


def start_watcher():

    init_database()

    observer = Observer()

    handler = LogHandler()

    observer.schedule(
        handler,
        path="logs",
        recursive=False
    )

    observer.start()

    print("=" * 55)
    print("PASSWORD SECURITY WATCHER")
    print("=" * 55)
    print("Status: RUNNING")
    print("Monitoring:", LOG_FILE)
    print("Press CTRL+C to stop")
    print("=" * 55)

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        observer.stop()

        print("Watcher stopped.")

    observer.join()


if __name__ == "__main__":
    start_watcher()
