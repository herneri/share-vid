"""
	main: Main Flask backend

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

from flask import Flask, render_template, redirect, url_for, request, session, flash, get_flashed_messages
import sqlite3
import database
from video import Video, videos_by_year, search_video

USER_DB = "share-vid.db"
connection = sqlite3.connect(USER_DB, check_same_thread=False)
cursor = connection.cursor()

# The years of the videos that the website will be providing
years = (2024, 2019, 2018, 2017, 2016, 2015, 2014)

app = Flask(__name__)
app.secret_key = "foo"

@app.route("/", methods=["POST", "GET"])
@app.route("/home/", methods=["POST", "GET"])
def home():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]

		status = database.check_user(username, password)
		if status == False:
			flash("Incorrect username or password", "error")
			return redirect(url_for("home"))

		session["username"] = username
		session["password"] = password
		return redirect(url_for("homepage", user=session["username"]))

	if "username" in session:
		return redirect(url_for("homepage", user=session["username"]))

	return render_template("index.html")

@app.route("/<user>/")
def homepage(user):
	if "username" not in session:
		flash("You are not logged in", "error")
		return redirect(url_for("home"))

	return render_template("homepage.html", user=user, years=years)

@app.route("/<year>-videos/")
def year(year):
	if "username" not in session:
		flash("You are not logged in", "error")
		return redirect(url_for("home"))

	videos = videos_by_year(year, cursor)
	if videos == []:
		flash(f"No videos from {year} have been found", "notice")
		return redirect(url_for("error", code=404))

	return render_template("year.html", year=year, videos=videos)

@app.route("/video/<video_name>")
def video(video_name):
	if "username" not in session:
		flash("You are not logged in", "error")
		return redirect(url_for("home"))
	
	video = search_video(video_name, cursor)
	if video == None:
		flash(f"Failed to find video titled \"{video_name}\"")
		return redirect(url_for("error", code=404))

	return render_template("video.html", title=video.name, year=video.year, path=video.path)

@app.route("/change-password/", methods=["POST", "GET"])
def change_pw():
	if request.method == "POST":
		username = request.form["username"]
		old_password = request.form["old_password"]
		new_password = request.form["new_password"]

		if len(new_password) < 8:
			flash("Password must be over 8 characters long", "error")
			return redirect(url_for("change_pw"))

		change_status = database.change_password(username, old_password, new_password)

		if change_status == True:
			flash("Password changed sucessfully!", "info")
			return redirect(url_for("home"))
		
		flash("Failed to change password, invalid username or old password entered", "error")
		return redirect(url_for("change_pw"))

	return render_template("change-pw.html")

@app.route("/error/<code>")
def error(code):
	msgs = get_flashed_messages()
	if not msgs:
		return redirect(url_for("home"))

	return render_template("error.html", msgs=msgs), code

@app.route("/logout/")
def logout():
	if "username" in session:
		session.pop("username", None)
		session.pop("password", None)
		flash("Logged out sucessfully", "notice")

	return redirect(url_for("home"))

if __name__ == "__main__":
	app.run(debug=True)
	connection.close()
