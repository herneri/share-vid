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

from main import connection, cursor, mongo_db

import pymysql
import pymongo

import bcrypt

def get_sql(sql_file_name):
	sql_file = open(sql_file_name)
	sql = sql_file.read()
	sql_file.close()

	return sql

def init_db():
	sql_statement = get_sql("sql/create-tables.sql")
	cursor.executemany(sql_statement)

	connection.commit()
	return

# Hashes and salts password for storage in database
def secure_password(password):
	byte_password = password.encode("utf-8")
	salt = bcrypt.gensalt()

	return bcrypt.hashpw(byte_password, salt), salt

def add_user(username, password):
    hashed_password, salt = secure_password(password)
    cursor.execute("INSERT INTO users(username, password, salt) VALUES(%s, %s, %s)", (username, hashed_password, salt))
    connection.commit()

    return

def check_user(username, password):
	cursor.execute("SELECT password, salt FROM users WHERE username = %s", (username))

	data = cursor.fetchone()
	if data == None:
		return False

	database_password, salt = data[0], data[1]
	input_password = bcrypt.hashpw(password.encode("utf-8"), salt)

	if database_password == input_password:
		return True

	return False

def change_password(username, old_password, new_password):
	if check_user(username, old_password) == False:
		return False

	hashed_password, salt = secure_password(new_password)

	cursor.execute("UPDATE users SET password = %s, salt = %s WHERE username = %s", (hashed_password, salt, username))
	connection.commit()
	if cursor.rowcount == 0:
		return False

	return True

def post_comment(mongo_db, session, video_id, comment_data):
	video_comments = mongo_db["comments"]

	comment_document = {
		"video_id": video_id,
		"user": session["username"],
		"data": comment_data
	}

	video_comments.insert_one(comment_document)
	return

def load_comments(mongo_db, video_id):
	video_comments = mongo_db["comments"]
	return video_comments.find({"video_id": video_id})
