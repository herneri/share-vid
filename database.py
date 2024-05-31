"""
	Copyright 2024 Eric Hernandez

    This file is part of ShareVid.

    ShareVid is free software: you can redistribute it and/or modify it under the terms of the GNU General
    Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

    ShareVid is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
    the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with ShareVid. If not, see <https://www.gnu.org/licenses/>.
"""

import sqlite3
from main import connection, cursor
from os import listdir
from os.path import isfile

def get_sql(sql_file_name):
	sql_file = open(sql_file_name)
	sql = sql_file.read()
	sql_file.close()

	return sql

def init_db():
	sql_statement = get_sql("sql/create-tables.mysql")
	cursor.execute(sql_statement)

	return

def check_user(username, password):
	sql_statement = f"SELECT username FROM users WHERE username = '{username}' AND password = '{password}'"
	result = cursor.execute(sql_statement)

	if result.fetchone():
		return True

	return False

def change_password(username, old_password, new_password):
	sql_statement = f"UPDATE users SET password = '{new_password}' WHERE username = '{username}' AND password = '{old_password}'"

	cursor.execute(sql_statement)
	connection.commit()
	if cursor.rowcount == 1:
		return True

	return False

def to_string(array):
	string = ""

	for char in array:
		string += char

	return string

def format_video_name(name, delimiter):
	new_name = ""

	for char in name:
		if char == delimiter:
			new_name += " "
			continue

		new_name += char

	return new_name

def parse_video_name(video_name):
	name = None
	extension = None
	year = None
	path = video_name
	
	buffer = []
	ignore_delimiter = True

	i = len(video_name) - 1
	while i >= 0:
		if video_name[i] == '.' and ignore_delimiter == True:
			if extension == None:
				extension = to_string(buffer)
			elif year == None:
				year = to_string(buffer)
				ignore_delimiter = False

			buffer = []
			i -= 1
			continue
		elif video_name[i] == '/':
			if name == None:
				name = format_video_name(to_string(buffer), '.')
				break

		buffer.insert(0, video_name[i])
		i -= 1

	return name, extension, year, path

def update_video_db():
	for video in listdir("static/videos/"):
		if isfile("static/videos/" + video):
			name, extension, year, path = format_video_name("static/videos/" + video)
			sql_statement = f"INSERT INTO videos(name, format, year, path) VALUES({name}, {extension}, {year}, {path});"
			cursor.execute(sql_statement)
			connection.commit()
	return

if __name__ == '__main__':
	pass
