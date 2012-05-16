#!/bin/bash
# Lithid

ARG=$1

PID=$(ps -ef |grep "/usr/share/cmcompiler/prog/$ARG.py" |grep -v grep |awk '{print $2}')
echo "$PID"
if [ ! -z $PID ]; then
	for x in $(pstree -a -s -p $PID |grep -v init |cut -d"," -f2 |cut -d" " -f1); do 
		kill -9 $x
	done
fi

exit 0
