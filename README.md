# Feature Request App
# Travis Millott

Create a virtualenv for python:

  virtualenv-2.7 --python=python2.7 PATH
  source PATH/bin/activate


Install dependencies

  pip install twisted
  pip install psycopg2


Update the settings.py file with the correct database user/pass


Create the database

  createdb -h localhost -p 5432 -U postgres iws


Run the template in the db directory in the database

  \i template.sql

Give permissions to the database user defined in settings.py

  GRANT ALL ON feature_requests TO USER;


Run server with 

  python PATHTOSERVER/server.py -p PORT &

