from app import app

import firebase_admin
from firebase_admin import credentials

# MySQL imports
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

# Send In Blue SMTP Imports
import sib_api_v3_sdk

import os

# Rows from cursors will always be of type dict || cursorclass=DictCursor
mysql = MySQL(cursorclass=DictCursor)

# MySQL configurations and Init
app.config['MYSQL_DATABASE_USER'] = os.environ['SYNDEO_DB_USER']
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['SYNDEO_DB_PASS']
app.config['MYSQL_DATABASE_DB'] = os.environ['SYNDEO_DB']
app.config['MYSQL_DATABASE_HOST'] = os.environ['SYNDEO_DB_HOST']
app.config['MYSQL_DATABASE_PORT'] = int(os.environ['SYNDEO_DB_PORT'])
mysql.init_app(app)


credentials = credentials.Certificate('firebase.json')
firebase_admin.initialize_app(credentials)

defaultProfilePic = "https://i.ibb.co/6HJGFPY/Screenshot-2021-08-04-134113.png"

domainName = "licet.ac.in"

syndeoClientURL = "https://syndeo-fe.herokuapp.com"


# SendInBlue Config and Init
mail_config = sib_api_v3_sdk.Configuration()
mail_config.api_key['api-key'] = os.environ["SIB_MAIL_KEY"]

# Uncomment below lines to configure API key authorization using: partner-key
# configuration = sib_api_v3_sdk.Configuration()
# configuration.api_key['partner-key'] = os.environ["STRETCH_SIB_MAIL_KEY"]
