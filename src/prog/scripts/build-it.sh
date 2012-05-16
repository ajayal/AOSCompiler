#!/bin/bash
CMC="$HOME/.cmcompiler"
export USE_CCACHE=1
device=${1}
repo_path=${2}
if [ -e $CMC/build.failed ]; then
	rm -rf $CMC/build.failed
fi

cd ${repo_path}
source build/envsetup.sh
brunch ${device}
STATUS=$(echo $?)
if [ ${STATUS} -ne 0 ]; then
	touch $CMC/build.failed
fi

exit 0
