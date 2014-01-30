'''watchdog script to move SQL to feldman install SQL_DATA dir'''

import os
import sys
import time
import shutil
import logging
import datetime
from os.path import join as pjoin
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import feldman
fd_install = os.path.dirname(feldman.__file__)
SQL_DATA_PATH = pjoin(fd_install,'SQL_DATA','CUSTOM_SQL')

suffixes = ('.sql','.sqlspec','.fsql','.bsqlspec')

def check_sql(sql_file):
    if sql_file.endswith(suffixes):
        return True
    else:
        pass

class SQLMoveEvent(FileSystemEventHandler):
    """Logs all the events captured."""



    def on_moved(self, event):
        super(SQLMoveEvent, self).on_moved(event)

        if event.is_directory:
            what = 'directory'
        else:
            what = 'file'
            if check_sql(event.src_path):
                pass

        logging.info("Moved %s: from %s to %s", what, event.src_path,
                     event.dest_path)

    def on_created(self, event):
        super(SQLMoveEvent, self).on_created(event)

        if event.is_directory:
            what = 'directory'
        else:
            what = 'file'
            if check_sql(event.src_path):
                logging.info("SQL FILE %s: %s", what, event.src_path)
                f_name =  os.path.basename(event.src_path)
                new_file = pjoin(SQL_DATA_PATH,f_name)
                shutil.copyfile(event.src_path,new_file)


        logging.info("Created %s: %s", what, event.src_path)

    def on_deleted(self, event):
        super(SQLMoveEvent, self).on_deleted(event)

        if event.is_directory:
            what = 'directory'
        else:
            what = 'file'
            if check_sql(event.src_path):
                pass

        logging.info("Deleted %s: %s", what, event.src_path)

    def on_modified(self, event):
        super(SQLMoveEvent, self).on_modified(event)

        if event.is_directory:
            what = 'directory'
        else:
            what = 'file'
            if check_sql(event.src_path):
                logging.info("SQL FILE %s: %s", what, event.src_path)
                f_name =  os.path.basename(event.src_path)
                new_file = pjoin(SQL_DATA_PATH,f_name)
                shutil.copyfile(event.src_path,new_file)

        logging.info("Modified %s: %s", what, event.src_path)

if __name__ == "__main__":
    now = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    DEBUG_FILE = pjoin('watchdog-%s.log' % (now))

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=DEBUG_FILE,
                        filemode='a+')

    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = SQLMoveEvent()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()