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
            _isMentor = request.form['isMentor']
            _designation = request.form['designation']
            _linkedinUrl = request.form['linkedInURL']
            _contactPref = request.form['contactPref']
            _languages = request.form['languages']
            _resumeLink = request.form['resumeLink']
            _areasOfInterest = request.form['areasOfInterest']
            _higherEd = request.form['higherEd']
            _licensesAndCerts = request.form['licensesAndCerts']
            _tags = request.form['tags']
            _profileURL = request.form['profileURL']
            _summary = request.form['summary']
            _country = request.form['country']
            _isActive = request.form['isActive']

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(
            f"INSERT INTO users(uid, fullName, email, designation, gender, dateOfBirth, batch, department, isMentor, mobile, contactPref, country, linkedInURL, resumeLink, summary, areasOfInterest, languages, higherEd, licensesAndCerts, isActive, profileURL ) VALUES('{_uid}','{_fullName}', '{_email}','{_designation}','{_gender}','{_dateOfBirth}','{_batch}','{_department}','{_isMentor}','{_mobile}','{_contactPref}','{_country}','{_linkedinUrl}','{_resumeLink}','{_summary}','{_areasOfInterest}','{_languages}','{_higherEd}', '{_licensesAndCerts}','{_isActive}','{_profileURL}')")
            conn.commit()
            tags=_tags.split(',')
            sql = f"INSERT INTO tags (uid, *) VALUES('{_uid}', %)"
            i = 1
            for tag in tags:
                print(tag)
                sql = sql.replace("*","tag"+ str(i) +",*")
                sql = sql.replace('%', "'"+tag+"'" +',%')
                i +=1
            sql = sql.replace(",*",'')
            sql = sql.replace(',%', '')
            print (sql)
            cursor.execute(sql)
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
