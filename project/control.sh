#/bin/bash

export gameenv=dev

P_DIR=$(cd `dirname $0`; pwd -P)
export PYTHONPATH=${PYTHONPATH}${P_DIR}


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
    while [ $2 -gt $(ps ax | egrep -c "${aaa}.*?$1") ]; do
	sleep 1
    done
}

shell() 
{
    ipython -i $P_DIR/script/myshell.py $1 $2 $3 $4
}

start()
{
    python -OO ${P_DIR}/wsgi.py --port=58500 --log_file_prefix=${P_DIR}/logs/aaa-58500.log & echo 'start success'
    python -OO ${P_DIR}/wsgi.py --port=58501 --log_file_prefix=${P_DIR}/logs/aaa-58500.log & echo 'start success'
    python -OO ${P_DIR}/wsgi.py --port=58502 --log_file_prefix=${P_DIR}/logs/aaa-58500.log & echo 'start success'
    python -OO ${P_DIR}/wsgi.py --port=58503 --log_file_prefix=${P_DIR}/logs/aaa-58500.log & echo 'start success'
    #supervisorctl -c supervisor.conf restart aaa:*
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

runscript()
{
    #LOAD_SOURCE=true
    SCRIPT_NAME="${P_DIR}/script/$1.py"

    if [ -r ${SCRIPT_NAME} ]; then
        python $SCRIPT_NAME $2 $3
        echo
        echo 'runscript done.'
    fi
}

case "$1" in 
    start) start;;
    stop) stop;;
    restart) restart;;
    runscript) runscript $2 $3 $4;;
    shell) shell $2 $3 $4;;
    *) shell $1 $2 $3 $4;;
        #echo "Usage $0 (start|stop|restart|shell)"
        #exit 1
        #;;
esac
    
