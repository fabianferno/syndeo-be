from app import app

import firebase_admin
from firebase_admin import credentials

# MySQL imports
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

# Rows from cursors will always be of type dict || cursorclass=DictCursor
mysql = MySQL(cursorclass=DictCursor)

# MySQL configurations and Init
app.config['MYSQL_DATABASE_USER'] = "tux"
app.config['MYSQL_DATABASE_PASSWORD'] = "licet@123"
app.config['MYSQL_DATABASE_DB'] = "fabian"
app.config['MYSQL_DATABASE_HOST'] = "opencloud.pattarai.in"
app.config['MYSQL_DATABASE_PORT'] = 8306
mysql.init_app(app)


credentials = credentials.Certificate('firebase.json')
firebase_admin.initialize_app(credentials)

defaultProfilePic = "https://i.ibb.co/6HJGFPY/Screenshot-2021-08-04-134113.png"

domainName = "licet.ac.in"