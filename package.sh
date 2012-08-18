#!/bin/bash
# Install this app

name="aoscompiler"

function install_fun() {

	ver=$(grep "Version" share/desktop/${name}.desktop |cut -d"=" -f2)
	dpkg -s debhelper &>> /dev/null

	if  [ $? -ne 0 ]; then
		echo ">>> ${name} needs to install devhelper <<<"
		sudo apt-get install debhelper
	fi

	type=$(dpkg-architecture |grep "DEB_BUILD_ARCH=" |cut -d"=" -f2)

	dpkg-buildpackage -rfakeroot
	sudo dpkg -i ../${name}_${ver}_${type}.deb

	if [ $? -ne 0 ]; then
		sudo apt-get install -f
	fi

}

function clean_fun() {

	rm -rf debian/$name/
	rm -rf debian/$name.substvars
	rm -rf debian/*.log
	rm -rf debian/files
	rm -rf debian/*debhelper

	rm -rf ../${name}_*
	
	echo "Cleaned"

}

arg_num=$#

if [ $arg_num -gt 1 ]; then
	echo "Error: Got ${arg_num}, looking for only one or less arguments. Try help..."
	exit 1
fi

arg=$1

case $arg in

	help )
		echo "${name} package installer/cleaner"
		echo "======"
		echo "package.sh clean | clean environment"
		echo "pacakge.sh install | install package"
		echo "package.sh | install then clean";;
	clean )
		clean_fun;;
	install )
		install_fun;;
	*)
		install_fun
		clean_fun;;

esac

exit 0
