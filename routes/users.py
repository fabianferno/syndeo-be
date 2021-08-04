import pymysql
from app import app, firebase_error, forbidden, internal_server_error
from config import mysql, defaultProfilePic
from flask import jsonify, request
from firebase_admin import auth



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
            # Create a new user
            
            _fullName = request.form['fullName']
            _email = request.form['email']
            _password = request.form['password']
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

            try:
                account = auth.create_user(
                        email=_email,
                        email_verified=False,
                        phone_number=_phoneNumber,
                        password=_password,
                        display_name=_fullName,
                        photo_url=defaultProfilePic,
                        disabled=False
                    )

                try: 
                    cursor.execute(
                    f"INSERT INTO users(uid, fullName, email, designation, gender, dateOfBirth, batch, department, isMentor, mobile, contactPref, country, linkedInURL, resumeLink, summary, areasOfInterest, languages, higherEd, licensesAndCerts, isActive, profileURL ) VALUES('{account.uid}','{_fullName}', '{_email}','{_designation}','{_gender}','{_dateOfBirth}','{_batch}','{_department}','{_isMentor}','{_mobile}','{_contactPref}','{_country}','{_linkedinUrl}','{_resumeLink}','{_summary}','{_areasOfInterest}','{_languages}','{_higherEd}', '{_licensesAndCerts}','{_isActive}','{_profileURL}')")
                    tags=_tags.split(',')
                    sql = f"INSERT INTO tags (uid, *) VALUES('{account.uid}', %)"
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

                except Exception as e:
                    auth.delete_user(account.uid)
                    conn.rollback()
                    print(e)
                    return internal_server_error(error = e)


            except Exception as e:
                auth.delete_user(account.uid)
                return firebase_error()

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
            print(profile)
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
