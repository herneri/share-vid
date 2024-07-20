"""
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

import sqlite3
from os import listdir
from os.path import isfile

# Character that seperates words in a video's name
delimiter = '_'

class Video:
	def __init__(self, id_num, name, year, path):
		self.id = id_num
		self.name = name
		self.year = year
		self.path = path

def search_video(name, cursor):
	result = cursor.execute("SELECT id, name, year, path FROM videos WHERE name = ?", (name,))
	data = result.fetchone()

	if not data:
		return None

	return Video(data[0], data[1], data[2], data[3])

def videos_by_year(year, cursor):
	videos = []

	results = cursor.execute("SELECT id, name, year, path FROM videos WHERE year = ?", (year,))
	for video in results.fetchall():
		video_object = Video(video[0], video[1], video[2], video[3])
		videos.append(video_object)

	return videos

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

	# Ignore delimiter while finding extension and year,
	# once found collect it when getting the video name
	ignore_delimiter = True
	buffer = []

	i = len(video_name) - 1
	while i >= 0:
		if ignore_delimiter == True and (video_name[i] == '.' or video_name[i] == delimiter):
			if extension == None:
				extension = to_string(buffer)
			elif year == None:
				year = to_string(buffer)
				ignore_delimiter = False

			buffer = []
			i -= 1
			continue
		# The video name ends here and
		# the path starts, all data is collected
		elif video_name[i] == '/':
			if name == None:
				name = format_video_name(to_string(buffer), delimiter)
				break

		buffer.insert(0, video_name[i])
		i -= 1

	return name, extension, year, path

def update_video_db(connection, cursor):
	for video in listdir("static/videos/"):
		if isfile("static/videos/" + video):
			name, extension, year, path = parse_video_name("videos/" + video)
			cursor.execute("INSERT INTO videos(name, format, year, path) VALUES(?, ?, ?, ?)", (name, extension, year, path))
			connection.commit()

	return
