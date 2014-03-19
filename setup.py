import os
import sys

if 'develop' in sys.argv:
    # Don't import setuptools unless the user is actively trying to do
    # something that requires it.
    from setuptools import setup
else:
  from distutils.core import setup
  import sys

curdir = os.path.abspath(os.path.dirname(__file__))
config_suffix_list = ["*.ini"]
catalog_suffix_list = ['*.sql',
                       '*.fsql',
                       '*.fdsql',
                       '*.msql',
                       '*.bsqlspec',
                       '*.sqlspec',
                       '*.py']

def get_sql_files():
    data_files = []

    root = os.path.join("data", "catalog", "SQL_DATA")
    for r, ds, fs in os.walk(root):
        path = r[r.find('SQL_DATA'):]
        sql_files = [os.path.join(path, suf) for suf in catalog_suffix_list]
        data_files = data_files + sql_files

    root = os.path.join("util", "config")
    for r, ds, fs in os.walk(root):
        path = r[r.find('config'):]
        ini_files = [os.path.join(path, suf) for suf in config_suffix_list]
        data_files = data_files + ini_files

    return data_files

package_data = dict(feldman=get_sql_files())
package_data['feldman'].append('trqadrc.ini')
package_data['feldman'].append('feldman.ini')

version = "0.0.1"
setup(name='thomson',
      version=version,
      author='Continuum Analytics',
      author_email='info@continuum.io',
      url='http://github.com/ContinuumIO/feldman',
      description='Python TRQAD API',
      packages=['thomson', 
                'thomson.data', 
                'thomson.util', 
                'thomson.test', 
                'thomson.array'],
      package_data=package_data,
      zip_safe=False,
      install_requires=['pandas>=0.12.0',
                        'numpy>=1.7.1',
                        'scipy>=0.12.0',
                        'arraymanagement>0.0.1',
                        'pytables>=3.0.0',
                        'sqlalchemy>=0.9.1',
                        'pyodbc>=3.0.7'])
