import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from move_files import *
""" move_files is the original program. If there is no need to rename file, use this import and
comment out sefaria"""
#from sefaria import *


def on_created(event):
    """
    :param event: watchdogevent type

    get file name from event, then runs move file function from move_files/sefaria
    """
    time.sleep(1)
    file_name = event.src_path.split("\\")[-1]  # gets file name from event called by observer
    move_file(source_folder, file_name)

def on_modified(event):
    on_created(event)
def main():
    """
    the watchdog checks source folder for created file.
    when created, runs on_created function above
    """
    patterns = "*"  # patterns is what files to handle.
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    # event handler handles events that was observed via observer
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    # initialize all events according to functions we made:
    my_event_handler.on_created = on_created
    my_event_handler.on_modified = on_modified

    # create an observer:
    path = source_folder
    go_recursively = False  # don't monitor also sub-directories, it causes issues..
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()


if __name__ == "__main__":
    main()
