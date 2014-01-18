import sys

if 'develop' in sys.argv:
    # Don't import setuptools unless the user is actively trying to do
    # something that requires it.
    from setuptools import setup

else:
  from distutils.core import setup
  import sys

__version__ = (0, 0, 1)

setup(
    name = 'feldman',
    version = '.'.join([str(x) for x in __version__]),
    author = 'Continuum Analytics',
    author_email = 'info@continuum.io',
    url = 'http://github.com/ContinuumIO/feldman',
    description = 'Python TRQAD API',
    packages = ['feldman'],
    package_data = {'feldman':['SQL_DATA/*.sql',
                               'SQL_DATA/*.fsql',
                               'SQL_DATA/*.bsqlspec',
                               'SQL_DATA/*.sqlspec',
                               'SQL_DATA/UNIVERSE_SQL/*',
                               'SQL_DATA/WORLDSCOPE/*',
                               'SQL_DATA/datalib/*',
                               'trqadrc.ini']},
    zip_safe=False,
    install_requires=['pandas>=0.12.0','numpy>=1.7.1',
                      'scipy=>0.12.0','arraymanagement>0.0.1',
                      'pytables=>3.0.0','sqlalchemy>=0.9.1',
                      'pyodbc>=3.0.7'
                    ],
)
