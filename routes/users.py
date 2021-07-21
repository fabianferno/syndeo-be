import pymysql
from app import app, forbidden, internal_server_error
from config import mysql
from flask import jsonify, request


@app.route('/users', methods=['POST', 'GET', 'PUT', 'DELETE'])
def manageUsers():
    """
        [POST] - Create a new profile
        [GET] - Get a profile under the given uid
    """
    try:
        _uid = request.form['uid']
        # if _uid and request.method == 'POST':
        #     # Create a new user

        #     _fullName = request.form['fullName']
        #     _email = request.form['email']
        #     _gender = request.form['gender']
        #     _mobile = request.form['mobile']
        #     _batch = request.form['batch']
        #     _department = request.form['department']
        #     _address = request.form['address']

        #     conn = mysql.connect()
        #     cursor = conn.cursor()

        #     cursor.execute(
        #         f"INSERT INTO users(uid, fullName, email, gender, mobile, batch, department, address, dateOfBirth, ) VALUES('{_uid}', '{_email}')")
        #     conn.commit()
        #     res = jsonify('success')
        #     res.status_code = 200
        #     return res

        if _uid and request.method == 'GET':
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT * FROM `users` WHERE `users`.`uid` = '{_uid}'")

            profile = cursor.fetchone()

            res = jsonify(profile)
            res.status_code = 200
            return res

        else:
            return forbidden()  # It throws a 403 response saying "failure"

    except Exception as e:
        print(e)
        return internal_server_error()

    finally:
        cursor.close()
        conn.close()
