
.. _installation:

############
Installation
############

Installing Estuarial is quite simple and has minimal dependencies.  We recommend installing with conda::

    $conda install estuarial

Alternatively, you can also pull the repo and install from source::

    $git clone https://github.com/ContinuumIO/estuarial.git
    $cd estuarial; python setup.py install

Configuration
-------------

When loading estuarial for the first time, it will check if a `~/.estuarial` directory exists your home.  If it does not
exist, one will automatically be created for you.  This directory houses credential files, configuration and log files,
as well as cache data.

Estuarial configuration relies on ODBC and as such requires connection info (stored in ini format) to be defined.  An
example ODBC auth file is laid out below:

Estuarial needs authentication and driver information to properly connect and execute queries against the DB.  By
default, Estuarial will load an INI file found here: ``install_path/site-packages/estuarial/util/config/estuarial.ini``.
You can override the default authentication/configuration by placing a similar file with the appropriate values in
``~/.estuarial/estuarial.ini``

The `estuarial.ini`` file should look like the following::

    [ESTUARIAL]
    Description = ODBC CONNECTION INFO FOR ESTUARIAL
    Trace      = Yes
    Port       = XXXX
    Server     = XX.XXX.XXX.XX
    Database   = XXX
    UserName   = XXXXXXX
    Password   = XXXXXXX
    Driver     = /XXXX/XXXX/XXXX.X.X
    Threading  = 1
    UsageCount = 1



Common values:

* PORT: `1433` (Standard SQL Server DB Port)
* Database: `qai`
* Driver
 - Centos/Redhat SQL Server Driver: `/opt/microsoft/sqlncli/lib64/libsqlncli-11.0.so.1790.0`
 - FreeTDS Driver: `/usr/local/lib/libtdsodbc.so.0.0.0`
 - Windows SQL Server Driver: `SQL Server`


Installing FreeTDS
------------------

To install FreeTDS from source::

    $wget ftp://ftp.freetds.org/pub/freetds/stable/freetds-stable.tgz
    $tar xzvf freetds-stable.tgz
    $cd freetds-0.XX/


    #linux
    $./configure --with-unixodbc=/usr --with-tdsver=8.0

    #OSX
    $./configure --with-iodbc=/usr --with-tdsver=8.0

    make -j4
    sudo make install

Driver will now be installed at `/usr/local/lib/libtdsodbc.so.0.0.0` on **linux** or `/usr/local/lib/libtdsodbc.so` on
**OSX**

Installing on Debian/Ubuntu::

    $aptitude install libdbd-freetds freetds-dev freetds-bin

    #debian
    $ls /usr/lib/x86_64-linux-gnu/dbd/libdbdfreetds.so

    #Ubuntu
    $ls /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so


To confirm FreeTDS is working properly start an ipython/python prompt::

    >>> import pyodbc

    >>> creds = {
        "Uid": USERNAME,
        "Pwd": PASSOWRD,
        "driver": THE DRIVER LISTED ABOVE,
        "server": ADDR,
        "port": 1433,
        }

    >>> conn = pyodbc.connect('Driver=%s;Server=%s;Database=qai;Uid=%s;Pwd=%s;\
                               TDS_VERSION=8.0;PORT=%s'%\
                               (creds['driver'], creds['server'],\
                               creds['Uid'],creds['Pwd'],creds['port']))

    >>> cur = conn.cursor()

    >>> cur.execute('select top 10 * from dbo.wsndata').fetchall()


