import logging
import datetime
import os
from os.path import join as pjoin
from os.path import join, dirname, split, realpath, exists
import shutil



log = logging.getLogger('feldman')
log.setLevel(logging.DEBUG)

USER=os.path.expanduser('~')
FELDMAN_DIR = pjoin(USER,'.feldman')
FELDMAN_LOG_DIR = pjoin(FELDMAN_DIR,'feldman-logs')
now = datetime.datetime.utcnow().strftime('%Y-%m-%d')

datalibdir = pjoin(dirname(__file__),'SQL_DATA','datalib')

if not os.path.exists(FELDMAN_DIR):
    print pjoin(dirname(__file__))
    shutil.copytree(datalibdir, pjoin(FELDMAN_DIR,'datalib'))
    shutil.copyfile(pjoin(dirname(__file__),'feldman.ini'),pjoin(FELDMAN_DIR,'feldman.ini'))

if not os.path.exists(FELDMAN_LOG_DIR):
    os.makedirs(FELDMAN_LOG_DIR)

DEBUG_FILE = pjoin(FELDMAN_LOG_DIR, 'feldman-%s.log' % (now))

#create file handler which logs even debug messages
fh = logging.FileHandler(DEBUG_FILE)
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(file_formatter)

console_formatter = logging.Formatter('>>> %(message)s')

ch.setFormatter(console_formatter)

# add the handlers to the logger
log.addHandler(fh)
log.addHandler(ch)
