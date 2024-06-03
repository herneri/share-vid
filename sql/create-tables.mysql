/*
	create-tables: Initialize tables for storing users and videos

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
*/

CREATE TABLE IF NOT EXISTS users(
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(10) NOT NULL,
	password VARCHAR(8) NOT NULL
);

CREATE TABLE IF NOT EXISTS videos(
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	format VARCHAR(5) NOT NULL,
	year INT NOT NULL,
	path VARCHAR(255) NOT NULL
);
