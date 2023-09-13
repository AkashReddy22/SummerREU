import re

import pymysql
from flask import Flask, redirect, render_template, request, session, url_for, jsonify
from flask_login import login_required, current_user
from flask_wtf import CSRFProtect

from extensions import bcrypt
from auth import add_login_routes

app = Flask(__name__)
app.debug = True

app.secret_key = "Summer12!"
bcrypt.init_app(app)
CSRFProtect(app)
add_login_routes(app)

class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "root"
        password = "Sairam12#"
        db = "summerREU"
    
        self.con = pymysql.connect(host=host, user=user, password=password, db = db, cursorclass = pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for logged in users
@app.route('/login/home')
@login_required
def home():
    # Check if the user is logged in
        # User is loggedin show them the home page
    return render_template('home.html', username=current_user.username)
    # User is not loggedin redirect to login page

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for logged in users
@app.route('/login/summerREU-New-Students')
@login_required
def summerREU_db_new():
    # Check if the user is logged in
    # We need all the account info for the user so we can display it on the profile page
    db = Database()
    cursor = db.cur
    cursor.execute('SELECT * FROM Users WHERE UserName = %s', current_user.username)
    account = cursor.fetchone()
    # Show the profile page with account info
    return render_template('summerREU-New-Students.html', account=account)
    # User is not logged in redirect to login page

@app.route('/login/search', methods=['GET', 'POST']) 
@login_required
def search():
    # if request.method == 'POST':
    #     # def get_person_table(self):
    db = Database()
    cursor = db.cur
    def get_unique_values_for_column(column):
        cursor = db.cur
        cursor.execute(f"SELECT DISTINCT {column} FROM Person")
        return [row[column] for row in cursor.fetchall()]
    
    query = """SELECT * FROM Person p 
                LEFT JOIN Ethinic e ON p.EthinicityID=e.EthinicID 
                LEFT JOIN MtbiInfo m ON p.PersonID=m.PersonID 
                """
    
    print(query)
    print(request.method)
    
    if request.method == 'POST':
        data = request.json
        column_to_filter = data.get('columnToFilter')
        filter_value = data.get('filterValue')
        if column_to_filter and filter_value != None:
            query += f"WHERE p.{column_to_filter} = %s "
            print(query)
            cursor.execute(query, (filter_value,))

    else:
        query += "ORDER BY GenderID, p.EthinicityID;"
        cursor.execute(query)

        
    print(query)
    data = cursor.fetchall()
    columns = list(data[0].keys()) if data else []

    # Close the cursor
    cursor.close()

    if request.method == 'POST':
        return jsonify(data)

    return render_template('search.html', data=data, columns=columns)

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
