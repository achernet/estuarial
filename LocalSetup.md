conda create -n trqad python=2.7
source activate trqad
conda install --file requirements_(OS).txt

##Install FreeTDS

###From SRC

```bash
wget ftp://ftp.freetds.org/pub/freetds/stable/freetds-stable.tgz
tar xzvf freetds-stable.tgz 

cd freetds-0.XX/

`./configure --with-odbc=/usr --with-tdsver=8.0`
make -j4
sudo make install```

Driver will now be installed at `/usr/local/lib/libtdsodbc.so.0.0.0`


###From DPKG Repo
aptitude install libdbd-freetds freetds-dev freetds-bin 

- debian
 - `/usr/lib/x86_64-linux-gnu/dbd/libdbdfreetds.so`

- ubuntu
 - `/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so`

*I've had good succes with installing from SRC*

##Testing setup

set local forwarding port in .ssh/config to something other than `2345-2347`.  This port number is used twice. 

 - LocalForward XXXX 10.143.14.62:1433
 - ProxyCommand  ssh -g -A quasiben@76.186.128.225 -L2345:127.0.0.1:XXXX nc %h %p 2> /dev/null


```python
creds = {
"Uid": "qas_test",
"Pwd": "qasqasqas",
"driver": "THE DRIVER LISTED ABOVE",
"server": "127.0.0.1",
"port": "XXXX",
}

conn = pyodbc.connect('Driver=%s;Server=%s;Database=qai;Uid=%s;Pwd=%s;TDS_VERSION=8.0;PORT=%s'%(creds['driver'],\
                             creds['server'],creds['Uid'],creds['Pwd'],creds['port']))

cur = conn.cursor()
cur.execute('select top 10 * from dbo.wsndata').fetchall()```


Example **felmdan-local-freedts.ini** config added to repo for ssh tunneling