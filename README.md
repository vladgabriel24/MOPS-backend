# MOPS-backend project

## Setting up the Database

Make sure to create a user to access the database accordingly. <br>
`CREATE USER '<username>'@'%' IDENTIFIED BY '<password>';`<br>
`GRANT ALL ON <username>.* TO '<username>'@'%';`<br>
`ALTER USER '<username>'@'%' IDENTIFIED WITH mysql_native_password BY '<password>';`<br>

Make sure to open the connections to the database. <br>
```
mariadbd --help --verbose
mariadbd  Ver 10.11.5-MariaDB for linux-systemd on x86_64 (MariaDB Server)
Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Starts the MariaDB database server.

Usage: ./mariadbd [OPTIONS]

Default options are read from the following files in the given order:
/etc/my.cnf /etc/mysql/my.cnf ~/.my.cnf
```

In the `/etc/my.conf` edit the following lines: <br>
```
[mysqld]
    ...
    skip-networking
    ...
    bind-address = 0.0.0.0
    ...
```

After everything has been configured, log in into mariaDB and run the scripts in the following order: <br>

`source ./db/database.sql;`<br>
`source ./db/database_config.sql;`<br>
`source ./db/load_database.sql;`<br>
or run
 `source /db/database-init.sql`

 ## Setting up the Backend
 Requirements: 
 1.You should have python installed on your system

 2.You should instal and activate the virtual environment (example for Linux)
 sudo apt install python3-venv python3-dev
 python3 -m venv venv
 source venv/bin/activate

 3.You should install Flask and SQLAlchemy
  pip install Flask
  pip install Flask-SQLAlchemy
  pip install mysql-connector-python
  pip install flask-cors


 4.You should modify line 10 (# Replace with your ip ) from /app/__init__.py
 5.You should run `python main.py` in venv to run the project



