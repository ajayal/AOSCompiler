#!/bin/bash
# Install this app

name="cmcompiler"

function install_fun() {

	ver=$(grep "Version" share/desktop/${name}.desktop |cut -d"=" -f2)
	chk=$(which dpkg-buildpackage |wc -l)
	type=$(dpkg-architecture |grep "DEB_BUILD_ARCH=" |cut -d"=" -f2)

	if  [ $chk -eq 0 ]; then
		sudo apt-get install debhelper
	fi

	dpkg-buildpackage -rfakeroot
	sudo dpkg -i ../${name}_${ver}_${type}.deb

}

function clean_fun() {

	rm -rf debian/$name/
	rm -rf debian/$name.substvars
	rm -rf debian/*.log
	rm -rf debian/files

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
