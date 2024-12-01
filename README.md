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
