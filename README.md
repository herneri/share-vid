# ShareVid

![ShareVid home page](/static/images/homepage.png)

A website of monolithic architecture to share videos with the
users you authorize on your instance.

## Features

1. Videos are organized by year
2. Metadata acquisition via the video's name
3. New users can only be added by the host
4. User authorization that is secure against SQL injections
5. Strong hashing and salting of user passwords
6. Instance management CLI utility (sv-mgmt.py)
7. Setup shell script (setup.sh)
8. Interactive configuration

## Configuration

The configuration file is in the JSON format at the path
`~/.config/sharevid-config.json`. You can manually write the
configuration file using the layout described below.
Alternatively, ShareVid will detect that there is no
configuration file and it will prompt you for each field
while writing the values in the file.

### JSON object layout

|     Key     |          Value          |      Type       |
|-------------|-------------------------|-----------------|
|     user    |     MySQL username      |     string      |
|     host    |     MySQL hostname      |     string      |
|   database  |     Database name       |     string      |
|    years    | Release years of videos | List of strings |
| secret\_key |    Flask Secret Key     |     string      |

## Dependencies

- Python 3.9 or newer
- Flask
- MySQL DBMS
- pymysql
- bcrypt (Python package)
