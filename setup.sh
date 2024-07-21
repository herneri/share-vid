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

if [ "$1" = "-h" ] || [ ! $1 ]; then
	printf "usage: setup.sh [VIDEO_DIRECTORY] \n"
	exit 0
fi

dependencies="python3 flask mysql httpd"
for dependency in $dependencies
do
	if ! which $dependency >> /dev/null; then
		printf "ERROR: $dependency is not installed \n"
		exit 1
	fi
done

mkdir static/videos
cp $1/* static/videos/

echo "CREATE DATABASE sharevid" | mysql
mysql sharevid < sql/create-tables.sql
echo "y" | ./sv-mgmt.py -u -v
