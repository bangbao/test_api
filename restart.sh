#!/bin/sh

P_DIR=$(pwd -P)
#pid_file=$P_DIR

#if [ -r $pid_file ]; then
#    kill -9 `cat $pid_file` &&
#    rm -rf -- "$pid_file" &&
#    sleep 1
#fi

for p in `ps aux|grep python| grep $P_DIR | grep -v grep |awk -F' ' '{print $2}'`
do
    sudo kill -9 $p && echo $p' killed'
done

python -O ${P_DIR}/wsgi.py --port=58500 --log_file_prefix=${P_DIR}/logs/mdota-58500.log & echo 'restart sucess'

#supervisorctl -c supervisor.conf restart mdota:*
