# Travis Millott

NGINX_CONF_DIR=PATH_TO_NGINX_CONF
MAIN_FOLDER=PATH_TO_STATIC_FILES


ESCAPED_MAIN_FOLDER="${MAIN_FOLDER//\//\\/}"
source ~/.iws/bin/activate

function deploy_production_static_files{
  sudo cp css/main.css /var/www/css/
  sudo cp js/main.js /var/www/js/
}

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


if [[ $(hostname -s) = ip-* ]]; then
  NGINX_PORT=80;
  deploy_production_static_files
  echo 'Production';
else
  NGINX_PORT=8880;
  echo 'Devel';
fi

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

