# Travis Millott

NGINX_CONF_DIR=REPLACE_WITHPATH
source ~/.iws/bin/activate

function stop_server {
  ps awwjx | grep python | grep server.py | awk '{print $2}' | sudo xargs kill -TERM
  /bin/sleep .5
  ps awwjx | grep python | grep server.py | awk '{print $2}' | sudo xargs kill -9

  procalive=`ps awwjx | grep python | grep server.py`
  if [ -n "$procalive" ]
    then
      echo 'Was not able to kill server.py'
  fi
  sudo nginx -s quit
  /bin/sleep .5
  ps awwjx | grep nginx | awk '{print $2}' | sudo xargs kill -9
}

function start_server {
  python server.py -p 5678 &
  sudo nginx -c $NGINX_CONF_DIR/nginx.conf
}

if [[ $1 == "" ]]; then
  stop_server
  start_server
  echo "Restarted";
elif [[ $1 == "stop" ]]; then
  stop_server
else
  echo "Try again"
fi

