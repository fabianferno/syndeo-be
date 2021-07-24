import pymysql
from app import app, forbidden, internal_server_error
from config import mysql
from flask import jsonify, request

#/mentees/mentors
@app.route('/mentees/mentors', methods=['GET'])
def getMentors():

    """
    [GET] - Get a list mentors under a menteeUid
    """
    try:
        if request.method == 'GET':
            _menteeUid = request.args['menteeUid']
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(f"SELECT `mentorUid` FROM `allocations` WHERE `allocations`.`menteeUid` = '{_menteeUid}'")
            mentors = cursor.fetchone()

            cursor.close()
            conn.close()

            res = jsonify(mentors)
            res.status_code = 200
            return res

        else:
            return forbidden()  # It throws a 403 response saying "failure"

    except Exception as e:
        print(e)
        return internal_server_error()