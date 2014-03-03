import sys
import os
from os.path import splitext, basename, join as pjoin

if 'develop' in sys.argv:
    # Don't import setuptools unless the user is actively trying to do
    # something that requires it.
    from setuptools import setup

else:
  from distutils.core import setup
  import sys

curdir = os.path.abspath(os.path.dirname(__file__))

suffix_list = ['*.sql','*.fsql','*.fdsql','*.msql','*.bsqlspec','*.sqlspec','*.py']
def get_sql_files():
    data_files = []
    root = pjoin("feldman","SQL_DATA")

    for r, ds, fs in os.walk(root):
        path = r[r.find('SQL_DATA'):]
        sql_files = [pjoin(path,suf) for suf in suffix_list]
        data_files = data_files+sql_files
    return data_files


package_data = dict(feldman=get_sql_files())
package_data['feldman'].append('trqadrc.ini')
package_data['feldman'].append('feldman.ini')

__version__ = (0, 0, 1)

setup(
    name = 'feldman',
    version = '.'.join([str(x) for x in __version__]),
    author = 'Continuum Analytics',
    author_email = 'info@continuum.io',
    url = 'http://github.com/ContinuumIO/feldman',
    description = 'Python TRQAD API',
    packages = ['feldman'],
    package_data = package_data,
    zip_safe=False,
    install_requires=['pandas>=0.12.0','numpy>=1.7.1',
                      'scipy=>0.12.0','arraymanagement>0.0.1',
                      'pytables=>3.0.0','sqlalchemy>=0.9.1',
                      'pyodbc>=3.0.7'
                    ],
)
