import pymysql
from app import app, forbidden, internal_server_error
from config import mysql
from flask import jsonify, request

# /mentors/mentees
@app.route('/mentors/mentees', methods=['GET'])
def getMentees():

    """
    [GET] - Get a list mentees under a mentorUid
    """
    try:
        if request.method == 'GET':
            _mentorUid = request.args['mentorUid']
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(f"SELECT * FROM `allocations` WHERE `allocations`.`mentorUid` = '{_mentorUid}'")
            
            mentees = cursor.fetchone()

            cursor.close()
            conn.close()
            
            res = jsonify(mentees)
            res.status_code = 200
            return res

        else:
            return forbidden()  # It throws a 403 response saying "failure"

    except Exception as e:
        print(e)
        return internal_server_error()


# /mentors/all
@app.route('/mentors/all', methods=['GET'])
def getAllMentors():
    
    """
        [GET] - Get a list of all mentors
    """
    try:
        if request.method == 'GET':

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM `users` WHERE `users`.`isMentor` = 1")
            mentorList = cursor.fetchone()

            cursor.close()
            conn.close()

            res = jsonify(mentorList)
            res.status_code = 200
            return res

        else:
            return forbidden()  # It throws a 403 response saying "failure"

    except Exception as e:
        print(e)
        return internal_server_error()

# /mentors/agree
@app.route('/mentors/agree', methods=['PUT'])
def isAgreed():
    
    """
        [PUT] - Sets an allocation as agreed
    """
    try:
        if request.method == 'PUT':
            _mentorUid = request.form['mentorUid']

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(f"UPDATE `allocations` SET `allocations`.`isAgreed`=1 WHERE `allocations`.`mentorUid`='{_mentorUid}'")

            conn.commit()
          
            res = jsonify('success')
            res.status_code = 200
            return res

        else:
            return forbidden()  # It throws a 403 response saying "failure"

    except Exception as e:
        print(e)
        return internal_server_error()