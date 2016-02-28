# Feature Request App
 Travis Millott

#### Create a virtualenv for python:

  `virtualenv-2.7 --python=python2.7 PATH`
  
  `source PATH/bin/activate`


#### Install dependencies

  `pip install twisted`

  `pip install psycopg2`


Update the settings.py file with the correct database user/pass


#### Install postgresql

  `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib`


#### Create and setup the database

  Change this file /var/lib/pgsql9/data/pg_hba.conf to have this line:
  ```
local   all             all                                     trust
```
  Change this file /var/lib/pgsql9/data/postgresql.conf to have:
```
    listen_addresses = 'localhost'
    port = 5432
```
  Setup the rest of the database:
  
  `sudo service postgresql start`
  Move into the database and add a password for the postgres user
  `sudo su - postgres`
  `psql -U postgres`
  `ALTER USER postgres WITH PASSWORD 'a_password_';`

  Create the user we're using to connect to the database with the username/password defined in settings.py
    `CREATE USER iws_user NOSUPERUSER;`
    `ALTER USER iws_user WITH PASSWORD 'another_password_';`

  Create and run the database for the app
  `CREATE DATABASE iws WITH OWNER iws_user;`
  `createdb -h localhost -p 5432 -U postgres iws`
  `sudo service postgresql initdb`

Run the template in the db directory in the database

  `\i db/template.sql`
  

Edit the restartServer.sh script's variables:

`MAIN_FOLDER` and `NGINX_CONF_DIR` with the directories of the main folder and the folder the nginx.conf file is in

Run server with 

  sh restartServer.sh

