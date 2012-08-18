#!/bin/bash

#   CMCompiler is free software. It comes without any warranty, to
#   the extent permitted by applicable law. You can redistribute it
#   and/or modify it under the terms of the Do What The Fuck You Want
#   To Public License, Version 2, as published by Sam Hocevar. See
#   http://sam.zoy.org/wtfpl/COPYING for more details.

CMC="$HOME/.cmcompiler"
CMC_CONF="$CMC/cmcompiler.cfg"
ADB=0

function chk_adb_running() {
chk_adb=$(adb devices 2>/dev/null |grep device |grep -v attached |wc -l)
if [ $chk_adb -ne 1 ]; then
	ADB=0
else
	ADB=1
fi
}

clear

chk_adb_running

if [ $ADB -eq 1 ]; then
	adb logcat
else
	echo "Adb is not running. Can't continue..."
fi
