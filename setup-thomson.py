import os
import sys

if 'develop' in sys.argv:
    # setuptools bad.
    from setuptools import setup
else:
  from distutils.core import setup

curdir = os.path.abspath(os.path.dirname(__file__))
config_suffix_list = ["*.ini"]
catalog_suffix_list = ('.sql',
                       '.fsql',
                       '.fdsql',
                       '.msql',
                       '.bsqlspec',
                       '.sqlspec',
                       '.py')

def get_sql_files():
    data_files = []

    root = os.path.join("thomson","data", "catalog", "SQL_DATA")
    install_folder = os.path.join("data", "catalog", "SQL_DATA")

    ##scan catalog for files with the above extensions and add to pkg_data_dirs
    for path, dirs, files in os.walk(root):
        for fs in files:
            if fs.endswith(catalog_suffix_list):

                #remove thomson from path name
                install_path = '/'.join(path.split('/')[1:])
                data_files.append(os.path.join(install_path,fs))

    return data_files


package_data = dict(thomson=get_sql_files())
package_data['thomson'].append('trqadrc.ini')
package_data['thomson'].append('feldman.ini')

version = "0.0.1"
setup(name='thomson',
      version=version,
      author='Continuum Analytics',
      author_email='info@continuum.io',
      url='http://github.com/ContinuumIO/feldman',
      description='Python TRQAD API',
      packages=['thomson',  
                'thomson.test', 
                'thomson.array',
                'thomson.util',
                'thomson.util.config',
                'thomson.data', 
                'thomson.data.query',
                'thomson.data.browse',
                'thomson.data.catalog',
                'thomson.data.drilldown'],
      package_data=package_data,
      zip_safe=False,
      install_requires=['pandas>=0.12.0',
                        'numpy>=1.7.1',
                        'scipy>=0.12.0',
                        'arraymanagement>0.0.1',
                        'pytables>=3.0.0',
                        'sqlalchemy>=0.9.1',
                        'pyodbc>=3.0.7'])
