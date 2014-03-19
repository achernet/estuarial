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

    root = os.path.join("estuary","data", "catalog", "SQL_DATA")
    install_folder = os.path.join("data", "catalog", "SQL_DATA")

    ##scan catalog for files with the above extensions and add to pkg_data_dirs
    for path, dirs, files in os.walk(root):
        for fs in files:
            if fs.endswith(catalog_suffix_list):

                #remove estuary from path name
                install_path = '/'.join(path.split('/')[1:])
                data_files.append(os.path.join(install_path,fs))

    return data_files


package_data = dict(estuary=get_sql_files())
package_data['estuary'].append('trqadrc.ini')
package_data['estuary'].append('estuary.ini')

version = "0.0.1"
setup(name='estuary',
      version=version,
      author='Continuum Analytics',
      author_email='info@continuum.io',
      url='http://github.com/ContinuumIO/estuary',
      description='Python TRQAD API',
      packages=['estuary',
                'estuary.test',
                'estuary.array',
                'estuary.util',
                'estuary.util.config',
                'estuary.data',
                'estuary.data.query',
                'estuary.data.browse',
                'estuary.data.catalog',
                'estuary.data.drilldown'],
      package_data=package_data,
      zip_safe=False,
      install_requires=['pandas>=0.12.0',
                        'numpy>=1.7.1',
                        'scipy>=0.12.0',
                        'arraymanagement>0.0.1',
                        'pytables>=3.0.0',
                        'sqlalchemy>=0.9.1',
                        'pyodbc>=3.0.7'])
