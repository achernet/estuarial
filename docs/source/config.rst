.. _config:

#############
Configuration
#############

When loading feldman for the first time, it will check if a `~/.feldman` directory exists your home.  If it does not
exist, one will automatically be created for you.  This directory houses credential files, configuration files for
Feldman, as well as all logs.

The Feldman configuration relies on ODBC and as such requires connection info (stored in ini format) to be defined.  An
example ODBC auth file is laid out below:

The ``~/.feldman/feldman.ini`` file should look like::

    [FELDMAN]
    Description = ODBC CONNECTION INFO FOR FELDMAN
    Trace      = Yes
    Port       = XXXX
    Server     = XX.XXX.XXX.XX
    Database   = XXX
    UserName   = XXXXXXX
    Password   = XXXXXXX
    Driver     = /opt/microsoft/sqlncli/lib64/libsqlncli-11.0.so.1790.0
    Threading  = 1
    UsageCount = 1



*Note: on Windows set **Driver = SQL Server** *



