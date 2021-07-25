import pymysql
from app import app, forbidden, internal_server_error
from config import mysql
from flask import jsonify, request

#/allocations
@app.route('/allocations',methods = ['POST'],['GET'])
def allocations():
"""    
    [POST] - Insert allocation records 
"""
    try:
        if _uid and request.method == 'POST':


            _uid = request.form['uid']
            _allocationId = request.form['allocationId']
            _mentorUid = request.form['mentorUid']
            _menteeUid = request.form['menteeUid']
            _dateAllocated = request.form['dateAllocated']
            _isValidated = request.form['isValidated']
            _isAgreed = request.form['isAgreed']
            _validator = request.form['validator']

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(
                f"INSERT INTO allocations(uid, allocationId, mentorUid, menteeUid, dateAllocated, isValidated, isAgreed, validator) VALUES('{_uid}','{_allocationId}', '{_mentorUid}', '{_menteeUid}', '{_dateAllocated}', '{_isValidated}', '{_isAgreed}', '{_validator}',)")
            conn.commit()
            res = jsonify('success')
            res.status_code = 200
            return res

"""
    [GET][admin] - Get a List of allocations
"""

        if request.method == 'GET':
            _allocationId = request.args['allocationId']
            
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM `admin` WHERE `admin`.`uid` = '{_uid}'")
                admin = cursor.fetchone()

            if admin: 
                cursor.execute(f"SELECT * FROM `allocations` WHERE `allocations`.`allocationId` = '{_allocationId}'")

            else:
                return forbidden()  # It throws a 403 response saying "failure"
                allocationRecord = cursor.fetchone()

                cursor.close()
                conn.close()

                res = jsonify(allocationRecord)
                res.status_code = 200
                return res

        else:
            return forbidden()  # It throws a 403 response saying "failure"

    except Exception as e:
        print(e)
        return internal_server_error()



#/allocations?<uid>

@app.route('/allocations?<uid>', methods = ['GET'])
def allocation(uid):

"""
    [GET][admin] - Get allocation record where mentorUid / menteerUid == uid
"""

try:
    if request.method == 'GET':
        _allocationId = request.args['allocationId']
            
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM `admin` WHERE `admin`.`uid` = '{_uid}'")
                admin = cursor.fetchone()

            if admin: 
                cursor.execute(f"SELECT * FROM `allocations` WHERE `allocations` . `mentorId` = '{_uid}' AND `menteeId` = '{_uid}' ")
            

            else:
                return forbidden()  # It throws a 403 response saying "failure"
                allocationRecord = cursor.fetchone()

                cursor.close()
                conn.close()

                res = jsonify(allocationRecord)
                res.status_code = 200
                return res

    else:
        return forbidden()  # It throws a 403 response saying "failure"

except Exception as e:
    print(e)
    return internal_server_error()
