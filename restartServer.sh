# Travis Millott

NGINX_CONF_DIR=REPLACE_WITH_NGINX_CONF_DIR
MAIN_FOLDER=REPLACE_WITH_MAIN_DIR
ESCAPED_MAIN_FOLDER="${MAIN_FOLDER//\//\\/}"

if [[ $(hostname -s) = ip-* ]]; then
  NGINX_PORT=80;
  echo 'Production';
else
  NGINX_PORT=8880;
  echo 'Devel';
fi

source ~/.iws/bin/activate

function stop_server {
  ps awwjx | grep python | grep server.py | awk '{print $2}' | sudo xargs kill TERM &> /dev/null
  /bin/sleep .5
  ps awwjx | grep python | grep server.py | awk '{print $2}' | sudo xargs kill 9 &> /dev/null

  procalive=`ps awwjx | grep python | grep server.py`
  if [ -n "$procalive" ]
    then
      echo 'Was not able to kill server.py'
  fi
  sudo nginx -s quit
  /bin/sleep .5
  ps awwjx | grep nginx | awk '{print $2}' | sudo xargs kill -9 &> /dev/null
}

function generateNginxFile {
  sed 's/NGINX_PORT/'"$NGINX_PORT"'/' nginx/nginx.conf | sed "s/MAIN_FOLDER/"$ESCAPED_MAIN_FOLDER"/" > $NGINX_CONF_DIR/nginx.run.conf
}

function start_server {
  python server.py -p 5678 &
  sudo nginx -c $NGINX_CONF_DIR/nginx.run.conf
}

if [[ $1 == "" ]]; then
  stop_server
  generateNginxFile
  start_server
  echo "Restarted";
elif [[ $1 == "stop" ]]; then
  stop_server
else
  echo "Try again"
fi

