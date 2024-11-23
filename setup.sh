#!/bin/sh
#	setup.sh: Setup configuration for ShareVid and initialize its database

#	Copyright 2024 Eric Hernandez

#	Licensed under the Apache License, Version 2.0 (the "License");
#	you may not use this file except in compliance with the License.
#	You may obtain a copy of the License at

#		https://www.apache.org/licenses/LICENSE-2.0

#	Unless required by applicable law or agreed to in writing, software
#	distributed under the License is distributed on an "AS IS" BASIS,
#	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#	See the License for the specific language governing permissions and
#	limitations under the License.

dependency_check() {
	local dependencies="python3 flask mysql httpd"

	for dependency in $dependencies
	do
		if ! which $dependency >> /dev/null; then
			printf "ERROR: $dependency is not installed \n"
			exit 1
		fi
	done

	return
}

import_videos() {
	if [ ! $1 ]; then
		printf "ERROR: Missing video directory \n"
		exit 1
	fi

	mkdir static/videos
	cp $1/* static/videos/

	return
}

create_database() {
	echo "CREATE DATABASE sharevid" | mysql
	mysql sharevid < sql/create-tables.sql
	echo "y" | ./sv-mgmt.py -u -v
	return
}

case "$1" in
	"-d")
		dependency_check
	;;

	"-i")
		import_videos $2
	;;

	"-c")
		create_database
	;;

	"-a")
		dependency_check
		import_videos $2
		create_database
	;;

	*)
		echo -e "usage: setup.sh [OPTION] [VIDEO_DIRECTORY]"
		echo -e "-a [VIDEO_DIRECTORY]\tDo all setup operations listed below"
		echo -e "-d\t\t\tCheck if dependencies are present"
		echo -e "-i [VIDEO_DIRECTORY]\tImport videos"
		echo -e "-c\t\t\tCreate ShareVid database"
		exit 0
	;;
esac
