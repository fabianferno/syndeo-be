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

            conn = mysql.connect()
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT * FROM `admin` WHERE `admin`.`uid` = '{_uid}'")

            admin = cursor.fetchone()

            if admin: 
                cursor.execute(f"UPDATE allocations SET allocations.isValidated=1 WHERE allocations.allocationId='{_allocationId}'")

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