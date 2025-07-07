import schedule
import time
import export_script
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#This line of code is for Schedule Pipeline Export
schedule.every().day.at("02:00").do(export_script.run_all_exports)

while True:
    schedule.run_pending()
    time.sleep(1)


#This line of code is for Event Trigger Pipeline Export
class FileTriggerHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".trigger"):
            print(f"Trigger file detected: {event.src_path}")
            export_script.run_all_exports()

observer = Observer()
observer.schedule(FileTriggerHandler(), path='watching_folder', recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
