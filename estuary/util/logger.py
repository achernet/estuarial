import os
import shutil
import logging
import datetime
from os.path import join as pjoin
from os.path import dirname, split, realpath, exists

log = logging.getLogger('estuary')
log.setLevel(logging.DEBUG)

USER = os.path.expanduser('~')
ESTUARY_DIR = pjoin(USER, '.estuary')
ESTUARY_LOG_DIR = pjoin(ESTUARY_DIR, 'estuary-logs')
now = datetime.datetime.utcnow().strftime('%Y-%m-%d')

datalibdir = pjoin(dirname(__file__), 'SQL_DATA', 'datalib')

if not os.path.exists(ESTUARY_DIR):
    print pjoin(dirname(__file__))
    shutil.copytree(datalibdir, pjoin(ESTUARY_DIR, 'datalib'))
    shutil.copyfile(pjoin(dirname(__file__), 'estuary.ini'),
                    pjoin(ESTUARY_DIR,'estuary.ini'))

if not os.path.exists(ESTUARY_LOG_DIR):
    os.makedirs(ESTUARY_LOG_DIR)

DEBUG_FILE = pjoin(ESTUARY_LOG_DIR, 'estuary-%s.log' % (now))

#create file handler which logs even debug messages
fh = logging.FileHandler(DEBUG_FILE)
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
file_formatter = logging.Formatter(format_str)
fh.setFormatter(file_formatter)

console_formatter = logging.Formatter('>>> %(message)s')
ch.setFormatter(console_formatter)

# add the handlers to the logger
log.addHandler(fh)
log.addHandler(ch)
