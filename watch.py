import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from move_files import *

# from sefaria import *

""" move_files is the original program. If there is no need to rename file, use this import and
comment out sefaria"""
"""
COMMENT OUT ON_MOVED OPTION IN MY_EVENT_HANDLER IF YOU ARE YEDIDYA!!!!
"""

# life cycle of chrome/firfox file:
# 1. created sample.crdownload file (oncreated called, but nothing happens cause of 'if' statement)
# 2. moved: src= sample.crdownload, dest = sample.temp  (onmoved called, but nothing happens cause of 'if' statement)
# 3. moved: src= sample.temp, dest = sample.pdf  (onmoved called, sends to move fun of dest path)
# 4. move_file of move_files.py called.

# life cycle of regular downloads:
# 1. created sample.pdf (oncreate called, sends to move fun of src path)
# 2. move_file of move_files.py called.


def on_created(event):
    # check if file is a temp file, and do nothing if so.
    if str(event.src_path).endswith((".crdownload", ".tmp")):
        return
    move(event.src_path)  # calls the move function with path

    """
    :param event: watchdogevent type

    get file name from event, then runs move file function from move_files/sefaria
    """


def on_moved(event):
    # not used for Yedidya because downloads work differently
    # check if file is a temp file, and do nothing if so.
    if str(event.dest_path).endswith((".crdownload", ".tmp")) or event.dest_path == event.src_path:
        return
    move(event.dest_path)  # Calls the move fun with DEST. this is because it is called AFTER it moved.


def move(src_path):
    # this function moves file using move_file.py
    # PARAMS : path of file that is defined by event

    if os.path.isdir(src_path):  # Don't do anything if file is a folder.
        return
    time.sleep(1)
    file_name = src_path.split("\\")[-1]  # gets file name from event called by observer
    move_file(source_folder, file_name)


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
    my_event_handler.on_moved = on_moved  # commented when on Yedidya's computer because it's unnecessary.

    # create an observer:
    src = source_folder
    go_recursively = False  # don't monitor also sub-directories, it causes issues..
    my_observer = Observer()
    my_observer.schedule(my_event_handler, src, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()


if __name__ == "__main__":
    main()
