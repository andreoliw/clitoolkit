#!/bin/bash
usage() {
	echo "USAGE: [$(dirname $0)/]$(basename $0) [options]
Restarts the wireless mouse module ('usbhid', in fact).
Use this after resuming from suspend mode on Ubuntu 12.10 (mouse is freezing, probably a bug).

OPTIONS
-h   Help"
	exit $1
}

while getopts "h" V_ARG ; do
	case $V_ARG in
		h)	usage 1 ;;
		?)	usage 2 ;;
	esac
done

sudo modprobe -r usbhid
sudo modprobe usbhid
