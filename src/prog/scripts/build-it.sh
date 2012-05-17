#!/bin/bash

#   CMCompiler is free software. It comes without any warranty, to
#   the extent permitted by applicable law. You can redistribute it
#   and/or modify it under the terms of the Do What The Fuck You Want
#   To Public License, Version 2, as published by Sam Hocevar. See
#   http://sam.zoy.org/wtfpl/COPYING for more details.

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
