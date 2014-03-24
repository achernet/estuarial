import os
import sys

if 'develop' in sys.argv:
    # setuptools bad.
    from setuptools import setup
else:
  from distutils.core import setup

curdir = os.path.abspath(os.path.dirname(__file__))
config_suffix_list = ["*.ini"]
catalog_suffix_list = ('.py',
                       '.yaml')

def get_sql_files():
    data_files = []

    root = os.path.join("estuarial","data", "catalog", "SQL_DATA")
    install_folder = os.path.join("data", "catalog", "SQL_DATA")

    ##scan catalog for files with the above extensions and add to pkg_data_dirs
    for path, dirs, files in os.walk(root):
        for fs in files:
            if fs.endswith(catalog_suffix_list):

                #remove estuarial from path name
                install_path = '/'.join(path.split('/')[1:])
                data_files.append(os.path.join(install_path,fs))

    return data_files


package_data = dict(estuarial=get_sql_files())
package_data['estuarial'].append('trqadrc.ini')
package_data['estuarial'].append('estuarial.ini')

version = "0.0.1"
setup(name='estuarial',
      version=version,
      author='Continuum Analytics',
      author_email='info@continuum.io',
      url='http://github.com/ContinuumIO/estuarial',
      description='Python TRQAD API',
      packages=['estuarial',
                'estuarial.test',
                'estuarial.array',
                'estuarial.util',
                'estuarial.util.config',
                'estuarial.data',
                'estuarial.query',
                'estuarial.browse',
                'estuarial.data.catalog',
                'estuarial.drilldown'],
      package_data=package_data,
      zip_safe=False,
      install_requires=['pandas>=0.12.0',
                        'numpy>=1.7.1',
                        'scipy>=0.12.0',
                        'arraymanagement>0.0.1',
                        'pytables>=3.0.0',
                        'sqlalchemy>=0.9.1',
                        'pyodbc>=3.0.7'])
