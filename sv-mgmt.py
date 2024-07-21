#!/usr/bin/env python3
"""
	sv-mgmt: CLI admin tool for managing a ShareVid instance
    
	Copyright (C) 2024  Eric Hernandez

    This file is part of ShareVid.

    ShareVid is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    ShareVid is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with ShareVid.  If not, see <https://www.gnu.org/licenses/>.
"""

from sys import argv, stderr
import sqlite3

import database
import video

argument_count = len(argv)
if (argument_count == 2 and argv[1] == "-h") or argument_count < 2:
	print("usage: sv-mgmt [OPERATION] [OBJECT]\n")
	print("-- Operations -- \n-a\tAdd\n\t-u\tUsers\n\t-v\tVideos \n\n-u\tUpdate\n\t-p\tPasswords\n\t-v\tVideo database")
	exit(0)

if argument_count < 3:
	stderr.write("sv-mgmt: Not enough arguments, use 'sv-mgmt -h' for help \n")
	exit(1)

if argv[1][0] != '-' or argv[2][0] != '-':
	stderr.write("sv-mgmt: Options must have a '-' before them \n")
	exit(2)

operation = argv[1]
operation_target = argv[2]

connection = sqlite3.connect("share-vid.db")
cursor = connection.cursor()

if operation == "-a":
	if operation_target == "-u":
		username = input("Enter username: ")
		password = input("Enter password: ")
		database.add_user(username, password)

		print(f"User, {username}, sucessfully created!")
elif operation == "-u":
	if argv[2] == "-v":
		print("WARNING: This will erase all current data on the video table,")
		print("it will also go through every video and insert them all. Are you sure you want to do this? [y/N]")
		user_choice = input()
		if user_choice == "" or user_choice == "N" or user_choice == "n":
			print("Video update operation aborted")
			exit(0)

		print("Deleting videos table...")
		cursor.execute("DROP TABLE videos")
		connection.commit()

		database.init_db()
		print("Updating videos table...")
		video.update_video_db(connection, cursor)
		print("Update complete")
	elif argv[2] == "-p":
		if len(argv) != 4:
			stderr.write("sv-mgmt: Username required for changing a password \n")
			exit(2)

		new_password = input("Enter new password: ")
		hashed_password, salt = database.secure_password(new_password)

		cursor.execute("UPDATE users SET password = ?, salt = ? WHERE username = ?", (hashed_password, salt, argv[3]))
		connection.commit()
		if cursor.rowcount == 0:
			stderr.write("sv-mgmt: Failed to change user's password \n")
			exit(3)

		print("Changed password for " + argv[3])
