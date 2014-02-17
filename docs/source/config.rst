.. _config:

#############
Configuration
#############

Feldman configuration relies on ODBC and as such requires connection info (stored in ini format) to be defined.  Feldman
looks for a `feldman.ini` file in the `~/.feldman` directory.  An example ODBC auth file is laid out below:

An example ``~/.feldman/feldman.ini`` file should look like::

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



Additionally, because Feldman uses ArrayManagement as the data exchange layer between Feldman and SQL Server, optional
configuration info can be defined in ~/.feldman/datalib/.  See ArrayManagement Docs for more info.