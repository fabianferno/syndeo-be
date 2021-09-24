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

            cursor.execute(
                f"SELECT * FROM `allocations` WHERE `allocations`.`mentorUid` = '{_mentorUid}'")

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
            cursor.execute(
                f"SELECT * FROM `users` WHERE `users`.`isMentor` = 1")
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


@app.route('/mentors/agree', methods=['PUT', 'POST'])
def isAgreed():
    """
        [POST] - Sets an allocation as agreed
    """
    try:
        if request.method == 'POST':
            _allocationId = request.form['allocationId']
            print("allocatonId: " + _allocationId)

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(
                f"UPDATE `allocations` SET `allocations`.`isAgreed`=1 WHERE `allocations`.`allocationId`='{_allocationId}'")

            conn.commit()

            res = jsonify('success')
            res.status_code = 200
            return res

    except Exception as e:
        print(e)
        return internal_server_error()


# /mentors/all
@app.route('/mentors', methods=['GET'])
def getMentorsUnderKeyword():
    """
        [GET] - Get a list of all mentors under a keyword
    """
    try:
        if request.method == 'GET':
            _keywords = request.args['keywords']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT `uid` FROM tags WHERE MATCH(`tag1`,`tag2`,`tag3`,`tag4`,`tag5`,`tag6`,`tag7`,`tag8`,`tag9`,`tag10`,`tag11`,`tag12`,`tag13`,`tag14`,`tag15`,`tag16`) AGAINST ('{_keywords}' IN NATURAL LANGUAGE MODE);")
            mentorKeywordMatchList = list(cursor.fetchall())

            # Also check for mentors matching name under given keywords
            cursor.execute(
                f"SELECT `uid` FROM users WHERE MATCH(`fullName`) AGAINST ('{_keywords}' IN NATURAL LANGUAGE MODE);")
            mentorNameMatchList = list(cursor.fetchall())

            # Combine the tuples
            mentorList = mentorKeywordMatchList + mentorNameMatchList

            # Init Result List
            resultProfiles = []

            for mentor in mentorList:
                try:
                    cursor.execute(
                        f"SELECT uid, fullName, designation, country FROM `users` WHERE `users`.`uid`='{mentor['uid']}' AND `users`.`isMentor` = 1 AND  `users`.`isActive` = 1")
                    profile = cursor.fetchone()
                    print(profile)
                    if(profile != None):
                        resultProfiles.append(profile)

                except Exception as e:
                    print(e)
                    return internal_server_error()

            cursor.close()
            conn.close()

            res = jsonify(resultProfiles)
            res.status_code = 200
            return res

        else:
            return forbidden()  # It throws a 403 response saying "failure"

    except Exception as e:
        print(e)
        return internal_server_error()
