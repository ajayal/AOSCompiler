#!/bin/bash

#   CMCompiler is free software. It comes without any warranty, to
#   the extent permitted by applicable law. You can redistribute it
#   and/or modify it under the terms of the Do What The Fuck You Want
#   To Public License, Version 2, as published by Sam Hocevar. See
#   http://sam.zoy.org/wtfpl/COPYING for more details.

ARG=$1

PID=$(ps -ef |grep "/usr/share/cmcompiler/prog/$ARG.py" |grep -v grep |awk '{print $2}')
echo "$PID"
if [ ! -z $PID ]; then
	for x in $(pstree -a -s -p $PID |grep -v init |cut -d"," -f2 |cut -d" " -f1); do 
		kill -9 $x
	done
fi

exit 0
