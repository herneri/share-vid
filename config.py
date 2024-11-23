"""
	config: Work with the ShareVid config file, which is JSON data

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

from json import dumps
from os import getenv

CONFIG_PATH = getenv("HOME") + ".config/sharevid-config.json"

def setup_config():
	config = {
		"user": None,
		"host": None,
		"database": None,
		"years": [],
		"secret_key": None
	}

	print(f"NOTICE: ShareVid config file not found at {CONFIG_PATH}, creating one...")
	config_file = open(CONFIG_PATH, "w")

	choice = input("Would you like to setup the configuration now? [y/N]: ")

	if choice.lower() != "y":
		print(f"sharevid requires a valid config file to function, set it up at {CONFIG_PATH}")
		config_file.write(dumps(config, indent=4))
		exit(0)

	for key in config.keys():
		if key == "years":
			print("Enter all the years this instance will show, type \"done\" when finished:")
			year = ""

			while True:
				year = input()
				if year.lower() == "done":
					break

				config["years"].append(year)

			continue

		config[key] = input(f"Enter value for the {key}: ")

	config_file.write(dumps(config, indent=4))
	config_file.close()
	return
