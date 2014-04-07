import os
import shutil
import logging
import datetime
import estuarial.data as etdata
from os.path import join as pjoin
from os.path import dirname, split, realpath, exists

log = logging.getLogger('estuarial')
log.setLevel(logging.DEBUG)

USER = os.path.expanduser('~')
ESTUARIAL_DIR = pjoin(USER, '.estuarial')
ESTUARIAL_LOG_DIR = pjoin(ESTUARIAL_DIR, 'estuarial-logs')
now = datetime.datetime.utcnow().strftime('%Y-%m-%d')

datalibdir = pjoin(etdata.__file__), 'catalog', 'SQL_DATA', 'datalib')

if not os.path.exists(ESTUARIAL_DIR):
    shutil.copytree(datalibdir, pjoin(ESTUARIAL_DIR, 'datalib'))
    shutil.copyfile(pjoin(dirname(__file__), 'estuarial.ini'),
                    pjoin(ESTUARIAL_DIR,'estuarial.ini'))

if not os.path.exists(ESTUARIAL_LOG_DIR):
    os.makedirs(ESTUARIAL_LOG_DIR)

DEBUG_FILE = pjoin(ESTUARIAL_LOG_DIR, 'estuarial-%s.log' % (now))

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
