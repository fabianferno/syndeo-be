import pymysql
from app import app, forbidden, internal_server_error
from config import mysql
from flask import jsonify, request

#/admin/validate
@app.route('/admin/validate', methods=['PUT'])
def adminValidate():
    
    """
        [PUT][admin] - Validates under allocation id
    """
    try:
        if request.method == 'PUT':
            _uid = request.form['uid']
            _allocationId = request.form['allocationId']
            _validator = request.form['validator']

            conn = mysql.connect()
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT * FROM `users` WHERE `users`.`uid` = '{_uid}' AND isAdmin = 1")

            admin = cursor.fetchone()

            if admin: 
                cursor.execute(f"UPDATE allocations SET allocations.isValidated=1, allocations.validator = '{_validator}' WHERE allocations.allocationId='{_allocationId}'")

            else:
                return forbidden()  # It throws a 403 response saying "failure"

            conn.commit()
            
            res = jsonify('success')
            res.status_code = 200
            return res

        else:
            return forbidden()  # It throws a 403 response saying "failure"

    except Exception as e:
        print(e)
        return internal_server_error()