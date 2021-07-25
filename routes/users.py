import pymysql
from app import app, forbidden, internal_server_error
from config import mysql
from flask import jsonify, request


@app.route('/users', methods=['POST', 'GET', 'PUT', 'DELETE'])
def manageUsers():
    """
        [POST] - Create a new profile
        [GET] - Get a profile under the given uid
        [PUT] - Update details and the given uid
        [DELETE] - Delete account for given uid
    """
    try:

        if request.method == 'POST':
            _uid = request.form['uid']
            # Create a new user
            
            _fullName = request.form['fullName']
            _email = request.form['email']
            _gender = request.form['gender']
            _dateOfBirth = request.form['dateOfBirth']
            _mobile = request.form['mobile']
            _batch = request.form['batch']
            _department = request.form['department']
            _type = request.form['type']
            _address = request.form['address']
            _linkedinUrl = request.form['linkedinUrl']
            _contactPref = request.form['contactPref']
            _languages = request.form['languages']
            _resumeLink = request.form['resumeLink']
            _areasOfInterest = request.form['_areasOfInterest']
            _higherEd = request.form['higherEd']
            _licensesAndCerts = request.form['licensesAndCerts']
            _tags = request.form['tags']
            _summary = request.form['summary']
            _country = request.form['country']
            _postalCode = request.form['postalCode']
            _isActive = request.form['isActive']

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(
            f"INSERT INTO users(uid, fullName, email, gender, dateOfBirth, mobile, batch, department, type, address, linkedUrl, contactPref, languages, resumeLink, areasOfInterest, higherEd, licensesAndCerts, tags, summary, country, postalCode, isActive ) VALUES('{_uid}','{_fullName}', '{_email}','{_gender}','{_dateOfBirth}','{_mobile}','{_batch}','{_department}','{_type}','{_address}','{_linkedinUrl}','{_contactPref}','{_languages}','{_resumeLink}','{_areasOfInterest}','{_higherEd}','{_licensesAndCerts}','{_tags}','{_summary}','{_country}','{_postalCode}','{_isActive}',)")
            conn.commit()
            res = jsonify('success')
            res.status_code = 200
            return res

            

        if request.method == 'GET':
            _uid = request.args['uid']

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT * FROM `users` WHERE `users`.`uid` = '{_uid}'")

            profile = cursor.fetchone()

            cursor.close()
            conn.close()

            res = jsonify(profile)
            res.status_code = 200
            return res


        if request.method == 'PUT':
            _uid = request.form['uid']
            

            conn = mysql.connect()
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT * FROM `users` WHERE `users`.`uid` = '{_uid}'")
            
            conn.commit()
            
            res = jsonify('success')
            res.status_code = 200
            return res

        if request.method == 'DELETE':
            _uid = request.form['uid']
            

            conn = mysql.connect()
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT * FROM `users` WHERE `users`.`uid` = '{_uid}'")
            
            conn.commit()

            res = jsonify('success')
            res.status_code = 200
            return res

        else:
            return forbidden()  # It throws a 403 response saying "failure"

    except Exception as e:
        print(e)
        return internal_server_error()
