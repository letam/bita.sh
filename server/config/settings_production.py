from .settings import *

with open("/var/www/bita.sh/secret_key.txt") as f:
	SECRET_KEY = f.read().strip()

DEBUG = False

STATIC_ROOT = "/var/www/bita.sh/static"
STATIC_URL = "/static/"

MEDIA_ROOT = "/var/www/bita.sh/uploads"
MEDIA_URL = "/uploads/"

ALLOWED_HOSTS = ["bita.sh"]


import dj_database_url
import urllib.parse
import os
import getpass

with open(f"/home/{os.environ.get('SUDO_USER') or getpass.getuser()}/.credentials/psql/bita_sh") as fd:
	credentials = {
		var: val.rstrip("\n")
		for var, val in [
			line.split("=", 1) for line in fd if "=" in line
		]
	}

# Encode every special character in value, for use in URLs
for k, v in credentials.items():
	if k in ["db_password"]:
		v = v.strip("'")
	credentials[k] = urllib.parse.quote(v)

db_user = credentials["db_user"]
db_password = credentials["db_password"]
db_host = credentials["db_host"]
db_name = credentials["db_name"]

if db_host == "localhost":
	db_host = ""

DATABASES["default"] = dj_database_url.parse(
	f"postgres://{db_user}:{db_password}@{db_host}/{db_name}"
)

