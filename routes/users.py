import pymysql
from app import app, forbidden
from config import mysql
from flask import jsonify, request


@app.route('users/register', methods=['POST'])
def registerUser():
    try:
        _uid = request.form['uid']
        _name = request.form['name']

        if _uid and _name and request.method == 'POST':
            # insert record in database
            sqlQuery = f"INSERT INTO users(uid,name) VALUES('{_uid}', '{_name}')"
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery)
            conn.commit()
            res = jsonify('success')
            res.status_code = 200
            return res
        else:
            return forbidden()

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


@app.route('users/search', methods=['GET'])
def searchUser():
    try:
        _keywords = request.form['keywords']

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * FROM `users` WHERE `users`.`name` = '{_keywords}'")
        rows = cursor.fetchall()
        res = jsonify(rows)
        res.status_code = 200
        return res

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
