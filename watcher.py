import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import Popen

# Customize the command to execute your script
command = [sys.executable, 'generate_cv.py']

class TemplateChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('template.html'):
            print('Template file has changed. Executing script...')
            process = Popen(command)
            process.communicate()

if __name__ == "__main__":
    event_handler = TemplateChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
