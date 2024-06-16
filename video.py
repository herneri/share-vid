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

class Video:
	def __init__(self, id_num, name, year, path):
		self.id = id_num
		self.name = name
		self.year = year
		self.path = path

def search_video(name, cursor):
	sql_statement = f"SELECT id, name, year, path FROM videos WHERE name = '{name}'"
	result = cursor.execute(sql_statement)
	data = result.fetchone()

	if not data:
		return None

	return Video(data[0], data[1], data[2], data[3])

def videos_by_year(year, cursor):
	sql_statement = f"SELECT id, name, year, path FROM videos WHERE year = {year}"
	videos = []

	results = cursor.execute(sql_statement)
	for video in results.fetchall():
		video_object = Video(video[0], video[1], video[2], video[3])
		videos.append(video_object)

	return videos
