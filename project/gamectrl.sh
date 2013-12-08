#/bin/bash

export gameenv=dev

P_DIR=$(pwd -P)


response_ok()
{
     echo $1
     status=$(curl --data "method=config.get_config&name=item" -w %{http_code} -s --output /dev/null "http://$1/api/")

     while [ $status != "200" ]; do
	 sleep 5
	 status=$(curl --data "method=config.get_config&name=item" -w %{http_code} -s --output /dev/null "http://$1/api/")
     done
}

check_pid_running()
{
    while [ $2 -gt $(ps ax | egrep -c "${GUNICORN_BIN}.*?$1") ]; do
	sleep 1
    done
}

shell() 
{
    ipython -i myshell.py
}

start()
{
    python -O ${P_DIR}/wsgi.py --port=58500 --log_file_prefix=${P_DIR}/logs/mdota-58500.log & echo 'start success'
    python -O ${P_DIR}/wsgi.py --port=58501 --log_file_prefix=${P_DIR}/logs/mdota-58500.log & echo 'start success'
    python -O ${P_DIR}/wsgi.py --port=58502 --log_file_prefix=${P_DIR}/logs/mdota-58500.log & echo 'start success'
    python -O ${P_DIR}/wsgi.py --port=58503 --log_file_prefix=${P_DIR}/logs/mdota-58500.log & echo 'start success'
    #supervisorctl -c supervisor.conf restart mdota:*
}

stop()
{
    for p in `ps aux | grep python | grep $P_DIR | grep -v grep | awk -F' ' '{print $2}'`  
    do
        sudo kill -9 $p && echo $p ' killed'
    done
}

restart()
{
    stop    
    start
}


case "$1" in 
    start) start;;
    stop) stop;;
    restart) restart;;
    shell) shell $2;;
    *) shell $2;;
        #echo "Usage $0 (start|stop|restart|shell)"
        #exit 1
        #;;
esac
    
