# For SMTP
from __future__ import print_function
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from config import mail_config

import pymysql
import random
from app import app, forbidden, internal_server_error
from config import mysql, syndeoClientURL
from flask import jsonify, request
import string
import datetime
import traceback


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# /allocations


@app.route('/allocations', methods=['POST', 'GET'])
def allocations():
    """
        [POST] - Insert allocation records
    """
    try:
        if request.method == 'POST':
            traceback.print_exc()
            _uid = request.form['uid']
            _mentorUid = request.form['mentorUid']
            _menteeUid = request.form['menteeUid']
            _menteeName = request.form['menteeName']
            _mentorName = request.form['mentorName']
            _mentorMail = request.form['mentorMail']
            _menteeSummary = request.form['menteeSummary']

            # Later
            _isValidated = 0
            _isAgreed = 0

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(
                f"INSERT INTO allocations(allocationId, mentorUid, menteeUid, dateAllocated, isValidated, isAgreed, validator) VALUES('{id_generator()}', '{_mentorUid}', '{_menteeUid}', NOW(), '{_isValidated}', '{_isAgreed}', NULL)")

            try:
                sendMenteeMail(_mentorName, _mentorMail,
                               _menteeSummary, _menteeName, syndeoClientURL + "/profile.php?uid=" + _menteeUid)

            except Exception as e:
                print(e)
                return internal_server_error()

            conn.commit()
            res = jsonify('success')
            res.status_code = 200
            return res

            # [GET][admin/mentor] - Get allocation record where mentorUid / menteeUid == uid

        elif request.method == 'GET':
            _uid = request.args['uid']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT * FROM `users` WHERE `users`.`uid`='{_uid}' AND `users`.`isMentor` = '1'")
            mentor = cursor.fetchone()

            if mentor:
                cursor.execute(
                    f"SELECT * FROM `allocations` WHERE `allocations`.`mentorUid` = '{_uid}' OR `allocations`.`menteeUid` = '{_uid}' ")

            else:
                # It throws a 403 response saying "failure"
                return {"status": "not a mentor"}

            allocationRecords = cursor.fetchall()
            cursor.close()
            conn.close()
            res = jsonify(allocationRecords)
            res.status_code = 200
            return res
        else:
            return forbidden()  # It throws a 403 response saying "failure"

    except Exception as e:
        print(e)
        return internal_server_error()


@app.route('/allocations/all', methods=['POST', 'GET'])
def get_allocations():
    """
        [GET] - Get complete allocations
    """
    try:
        if request.method == 'GET':
            _uid = request.args['uid']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT * FROM `users` WHERE `users`.`uid`='{_uid}' AND `users`.`isAdmin` = '1'")
            admin = cursor.fetchone()

            if admin:
                cursor.execute(
                    f"SELECT * FROM `allocations` WHERE `isAgreed`='1'")

            else:
                # It throws a 403 response saying "failure"
                return {"status": "not-admin"}

            allocationRecords = cursor.fetchall() 

            for record in allocationRecords: 
                fullNames = {"mentorName" : "", "menteeName" : ""} 
                cursor.execute(f"SELECT fullName FROM `users` WHERE `uid`='{record['mentorUid']}'")
                fullNames["mentorName"] = cursor.fetchone()["fullName"]

                cursor.execute(f"SELECT fullName FROM `users` WHERE `uid`='{record['menteeUid']}'")
                fullNames["menteeName"] = cursor.fetchone()["fullName"]

                record.update(fullNames)

            cursor.close()
            conn.close()
            res = jsonify({"status": "admin", "data" : allocationRecords})
            res.status_code = 200
            return res
        else:
            return forbidden()  # It throws a 403 response saying "failure"

    except Exception as e:
        print(e)
        return internal_server_error()


def sendMenteeMail(mentorName, mentorMail,
                   menteeSummary, menteeName, menteeProfileUrl):
    print("Sending Mentee Mail")
    print(mentorName)
    print(mentorMail)
    print(menteeSummary)
    print(menteeName)
    print(menteeProfileUrl)

    # create an instance of the API class
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(mail_config))
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{
            "email": mentorMail,
            "name": mentorName}],
        template_id=3,
        params={
            "mentee_summary": menteeSummary,
            "mentee": menteeName,
            "mentor": mentorName,
            "mentee_profile_url": menteeProfileUrl,
        },
        headers={
            "X-Mailin-custom": "custom_header_1:custom_value_1|custom_header_2:custom_value_2|custom_header_3:custom_value_3",
            "charset": "iso-8859-1"
        }
    )  # SendSmtpEmail | Values to send a transactional email

    try:
        # Send a transactional email
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)

    except ApiException as e:
        raise("Send In Blue Error",
              f"Exception when calling SMTPApi->send_transac_email: {e}\n")
