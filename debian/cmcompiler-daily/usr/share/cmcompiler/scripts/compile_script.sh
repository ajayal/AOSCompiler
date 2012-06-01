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

echo "Starting Cyanogenmod Compiler"
device=$(grep device $CMC_CONF |awk '{print $3}')
repo_path=$(grep repo_path $CMC_CONF |awk '{print $3}')
branch=$(grep branch $CMC_CONF |awk '{print $3}')
manuf=$(grep manuf $CMC_CONF |awk '{print $3}')
make_jobs=$(grep make_jobs $CMC_CONF |awk '{print $3}')

if [ "$make_jobs" == "Default" ]; then
        make_jobs=$(grep -c ^processor /proc/cpuinfo)
fi

if [ "$repo_path" == "Default" ]; then
        repo_path="$CMC/build"
fi

cd $repo_path

if [ ! -d device/$manuf/$device ]; then
        python build/tools/roomservice.py cm_$device
fi

if [ ! -d vendor/$manuf/$device/proprietary ]; then
        chk_adb_running
        if [ $ADB -eq 1 ]; then
                cd device/$manuf/$device
                sh extract-files.sh
                cd $repo_path
        else
                echo "Adb is not running. Needed to extract-files"
                exit 1
        fi
fi

if [ "$branch" == "ics" ]; then
        export USE_CCACHE=1
        if [ ! -f $CMC/cacheran ]; then
                /bin/bash prebuilt/linux-x86/ccache/ccache -M 50G
                touch $CMC/cacheran
        fi
fi

source build/envsetup.sh
brunch ${device}
