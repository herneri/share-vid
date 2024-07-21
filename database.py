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
from main import connection, cursor

import bcrypt

def get_sql(sql_file_name):
	sql_file = open(sql_file_name)
	sql = sql_file.read()
	sql_file.close()

	return sql

def init_db():
	sql_statement = get_sql("sql/create-tables.sql")
	cursor.executescript(sql_statement)

	connection.commit()
	return

# Hashes and salts password for storage in database
def secure_password(password):
	byte_password = password.encode("utf-8")
	salt = bcrypt.gensalt()

	return bcrypt.hashpw(byte_password, salt), salt

def add_user(username, password):
    hashed_password, salt = secure_password(password)
    cursor.execute("INSERT INTO users(username, password, salt) VALUES(?, ?, ?)", (username, hashed_password, salt))
    connection.commit()

    return

def check_user(username, password):
	result = cursor.execute("SELECT password, salt FROM users WHERE username = ?", (username,))

	data = result.fetchone()
	database_password, salt = data[0], data[1]
	input_password = bcrypt.hashpw(password.encode("utf-8"), salt)

	if database_password == input_password:
		return True

	return False

def change_password(username, old_password, new_password):
	if check_user(username, old_password) == False:
		return False

	hashed_password, salt = secure_password(new_password)

	cursor.execute("UPDATE users SET password = ?, salt = ? WHERE username = ?", (hashed_password, salt, username))
	connection.commit()
	if cursor.rowcount == 0:
		return False

	return True
