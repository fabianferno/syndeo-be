from routes.allocations import allocations
from flask.helpers import send_file
import pymysql
from app import app, firebase_error, forbidden, internal_server_error
from config import mysql, defaultProfilePic, domainName
from flask import jsonify, request
from firebase_admin import auth
import base64
from base64 import b64encode
from PIL import Image
import io 


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

@app.route('/users/pic', methods=['GET'])
def getProfilePic():
    """
        
        [GET] - Get a profile picture under the given uid
    """
    if request.method == 'GET':            
        _uid = request.args['uid']
        
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT `profilePic` FROM `users` WHERE `users`.`uid` = '{_uid}'")

            profilePicData = cursor.fetchone()
            profilePicData = profilePicData["profilePic"]
            print(profilePicData)

            cursor.close()
            conn.close()

            # Convert the bytes into a PIL image
            image = Image.open(io.BytesIO(profilePicData))

            img_io = io.StringIO()
            image.save(img_io, 'JPEG', quality=70)
            img_io.seek(0)
            return send_file(img_io, mimetype='image/jpeg')

        except Exception as e:
            print(e)
            return internal_server_error()



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
            _summary = request.form['summary']
            _country = request.form['country']
            _isActive = request.form['isActive']
            _profilePicFile = None

            if 'profilePic' in request.files:
                # Profile Pic File
                _profilePicFile = request.files['profilePic'].read()
                
                # We must encode the file to get base64 string
                _profilePicFile = base64.b64encode(_profilePicFile)

            # Check if the student is from licet
            if(_isMentor == '0'):
                domain = _email.split("@") 
                if domain[1] != domainName:
                    return forbidden()

            conn = mysql.connect()
            cursor = conn.cursor()

            try:
                account = auth.create_user(
                        email=_email,
                        email_verified=True,
                        phone_number=_mobile,
                        password=_password,
                        display_name=_fullName,
                        photo_url=defaultProfilePic,
                        disabled=False
                    )

                try: 
                    data = (account.uid, _fullName, _email, _designation, _gender, _dateOfBirth, _batch, _department, _isMentor, _mobile, _contactPref, _country, _linkedinUrl, _resumeLink, _summary, _areasOfInterest, _languages, _higherEd, _licensesAndCerts, _isActive, _profilePicFile)
                    query = "INSERT INTO users(uid, fullName, email, designation, gender, dateOfBirth, batch, department, isMentor, mobile, contactPref, country, linkedInURL, resumeLink, summary, areasOfInterest, languages, higherEd, licensesAndCerts, isActive, profilePic ) " \
                        "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"
                    cursor.execute(query, data)
                    
                    
                    tags=_tags.split(',')
                    sql = f"INSERT INTO tags (uid, *) VALUES('{account.uid}', %)"
                    i = 1
                    for tag in tags:
                        print(tag)
                        sql = sql.replace("*","tag"+ str(i) +", *")
                        sql = sql.replace('%', "'"+tag+"'" +', %')
                        i +=1
                    sql = sql.replace(", *",'')
                    sql = sql.replace(', %', '')
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
                print("firebase-error")
                print(e)
                json_dict = {
                    "status": "fail",
                    "reason": str(e)
                }
                res = jsonify(json_dict)
                res.status_code = 301
                return res

        if request.method == 'GET':
            _uid = request.args['uid']
            _profileUid = request.args['profileUid']

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(f"SELECT * FROM `users` WHERE `users`.`uid` = '{_profileUid}'")
            profile = cursor.fetchone()

            if profile['profilePic'] != None:
                image = b64encode(profile['profilePic']).decode("utf-8")
                profile['profilePic'] = image 

            if _uid != _profileUid:
                connectionDetails = {"allocation" : {}}
                connectionDetails["allocation"]["isAllocated"] = False
                cursor.execute(f"SELECT * FROM `allocations` WHERE (`mentorUid` = '{_uid}' AND `menteeUid` = '{_profileUid}') OR (`menteeUid` = '{_uid}' AND `mentorUid` = '{_profileUid}')")
                allocation = cursor.fetchone()  
                if allocation != None: 
                    connectionDetails["allocation"]["isAllocated"] = True
                    connectionDetails["allocation"]["allocationId"] = allocation["allocationId"]
                    connectionDetails["allocation"]["status"] = "Validated" if allocation["isValidated"] else ("mentorAgreed" if allocation["isAgreed"] else "pendingRequest") 
                profile.update(connectionDetails) 


            cursor.close()
            conn.close()

            res = jsonify(profile)
            res.status_code = 200
            return res


        if request.method == 'PUT':
            _uid = request.form['uid']
            
            if 'isActive' in request.form:
                conn = mysql.connect()
                cursor = conn.cursor()

                cursor.execute(
                f"UPDATE users SET isActive='{request.form['isActive']}' WHERE uid= '{_uid}'")

                conn.commit()
            else:
                _fullName = request.form['fullName']
                _email = request.form['email']
                _gender = request.form['gender']
                _dateOfBirth = request.form['dateOfBirth']
                _mobile = request.form['mobile']
                _batch = request.form['batch']
                _department = request.form['department']

                _designation = request.form['designation']
                _linkedinUrl = request.form['linkedInURL']
                _contactPref = request.form['contactPref']
                _languages = request.form['languages']
                _resumeLink = request.form['resumeLink']
                _areasOfInterest = request.form['areasOfInterest']
                _higherEd = request.form['higherEd']
                _licensesAndCerts = request.form['licensesAndCerts']
                _tags = request.form['tags']
                
                _summary = request.form['summary']
                _country = request.form['country']
                _profilePicFile = None
                

                conn = mysql.connect()
                cursor = conn.cursor()

                if 'profilePic' in request.files:
                    # Profile Pic File
                    _profilePicFile = request.files['profilePic'].read()
                    
                    # We must encode the file to get base64 string
                    _profilePicFile = base64.b64encode(_profilePicFile)

                cursor.execute(
                f"UPDATE users SET fullName='{_fullName}',designation='{_designation}',gender='{_gender}',dateOfBirth='{_dateOfBirth}',batch='{_batch}',department='{_department}',mobile='{_mobile}',contactPref='{_contactPref}',country='{_country}',linkedInURL='{_linkedinUrl}',resumeLink='{_resumeLink}',summary='{_summary}',areasOfInterest='{_areasOfInterest}',languages='{_languages}',higherEd='{_higherEd}',licensesAndCerts='{_licensesAndCerts}',profilePic='{_profilePicFile}' WHERE uid= '{_uid}'")
                conn.commit()
                
                sql = f"DELETE from `tags` WHERE uid = '{_uid}'"
                
                
                cursor.execute(sql)
                conn.commit()
                tags=_tags.split(',')
                sql = f"INSERT INTO tags (uid, *) VALUES('{_uid}', %)"
                i = 1
                for tag in tags:
                        print(tag)
                        sql = sql.replace("*","tag"+ str(i) +", *")
                        sql = sql.replace('%', "'"+tag+"'" +', %')
                        i +=1
                sql = sql.replace(", *",'')
                sql = sql.replace(', %', '')
                print (sql)
                cursor.execute(sql)
                conn.commit()

            res = jsonify('success')
            res.status_code = 200
            return res


        if request.method == 'DELETE':
            _uid = request.form['uid']

            conn = mysql.connect()
            cursor = conn.cursor()
            
            cursor.execute(f"DELETE FROM `tags` WHERE `tags`.`uid` = '{_uid}'")
            
            try:
                cursor.execute(f"DELETE FROM `users` WHERE `users`.`uid` = '{_uid}'")

            except Exception as e:
                
                conn.rollback()
                print(e)
                return internal_server_error(error = e)

            conn.commit()
            
            auth.delete_user(_uid)
            print('Successfully deleted user')

            res = jsonify('success')
            res.status_code = 200
            return res

        else:
            return forbidden()  # It throws a 403 response saying "failure"

    except Exception as e:
        print(e)
        return internal_server_error()

@app.route('/users/auth-status', methods=['POST'])
def authStatus():
    """
       
    """
    if request.method == 'POST':            
        _uid = request.form['uid']
        _idToken = request.form['idToken']
        
        try:
            var = authenticate(_uid, _idToken)

            if var == "Mentor" or var == "Student": 

                sql_query = f"SELECT profilePic, isActive FROM `users` WHERE uid = '{_uid}'"
                cnx = mysql.connect()
                cursor = cnx.cursor()
                cursor.execute(sql_query)
                row = cursor.fetchone()

                if row['profilePic'] != None:
                    image = b64encode(row['profilePic']).decode("utf-8")
                    row['profilePic'] = image

                result = { "authStatus": "true", "userType": var, "profilePic": row['profilePic'], "isActive": row['isActive'] }
                res = jsonify(result)
                res.status_code = 200
                return res

            elif var == "admin": 

                result = { "authStatus": "true", "userType": "admin" }
                res = jsonify(result)
                res.status_code = 200
                return res

            else:
                res = jsonify({ "authStatus": "false"})
                res.status_code = 200
                return res

        except Exception as e:
            print(e)
            return internal_server_error()


# Authentication method for reuse: returns "true", "false", or "invalid-data" || String values, not Boolean
def authenticate(_uid, _id_token):
    try:
        decoded_token = auth.verify_id_token(_id_token)
        uid = decoded_token['uid']
    except Exception as e:
        print(e)
        print("auth:invalid-data")
        return "invalid-data"

    try:
        # Check if ADMIN
        sql_query = f"SELECT * FROM `users` WHERE uid = '{_uid}' and isAdmin = 1"
        cnx = mysql.connect()
        cursor = cnx.cursor()
        cursor.execute(sql_query)
        row = cursor.fetchone()
        if row:
            uid = row['uid']
            if _uid == uid:
                return "admin"
        else:
            # Check if USER
            sql_query = f"SELECT * FROM `users` WHERE uid = '{_uid}'"
            cnx = mysql.connect()
            cursor = cnx.cursor()
            cursor.execute(sql_query)
            row = cursor.fetchone()
            if row:
                userType = row['isMentor']
                if userType == 1: 
                    return "Mentor"
                else:
                    return "Student"
            else:
                print("auth:fail")
                return "false"

    except Exception as e:
        print(e)
        return "false"