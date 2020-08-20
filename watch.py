import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from move_files import *



def on_created(event):
    file_name = event.src_path.split("\\")[1] # gets file name from event called by observer
    move_file(source_folder, file_name)


if __name__ == "__main__":
    patterns = "*"  # patterns is what files to handle.
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    # event handler handles events that was observed via observer
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    # initialize all events according to functions we made:
    my_event_handler.on_created = on_created

    # create an observer:
    path = "C://Users//user//Downloads"
    go_recursively = True # monitor also sub-directories
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()