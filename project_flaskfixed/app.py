from flask import Flask, request, jsonify, redirect, url_for
from flask import render_template
import mysql.connector
import hashlib

password1=input("Enter mysql database password: ")
app = Flask(__name__)


from prettytable import PrettyTable

hostname = "localhost"
username = "root"
password = password1
database = "iss_project"

def create_tables():
    try:
        connection = mysql.connector.connect(
            host=hostname,
            user=username,
            password=password,
            database=database
        )

        if connection.is_connected():
            cursor=connection.cursor()
            query="""CREATE TABLE  IF NOT EXISTS user_details(
                name varchar(1000),
                user_name varchar(1000) ,
                email varchar(1000) ,
                password varchar(1000) ,
                user_id INT AUTO_INCREMENT PRIMARY KEY);"""
            cursor.execute(query)
            connection.commit()
            query="""CREATE TABLE  IF NOT EXISTS  images(
            image_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT  ,
            image LONGBLOB,
            metadata varchar(1000)
            );"""
            cursor.execute(query)
            connection.commit()
            query="""CREATE TABLE  IF NOT EXISTS audio(
                audio_id INT AUTO_INCREMENT PRIMARY KEY,
                audio_data LONGBLOB,
                audio_metadata varchar(1000)
            );"""
            cursor.execute(query)
            connection.commit()
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection closed")

def insert_data(name1,username1, email1, password1):
    try:
        connection = mysql.connector.connect(
            host=hostname,
            user=username,
            password=password,
            database=database
        )

        if connection.is_connected():
            cursor = connection.cursor()
            query = "INSERT INTO user_details (name,user_name, email, password) VALUES (%s,%s, %s, %s)"
            data = (name1,username1, email1, password1)
            cursor.execute(query, data)
            connection.commit()

            print("Data inserted successfully!")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection closed")

def print_table_from_mysql():
    try:
        connection = mysql.connector.connect(
            host=hostname,
            user=username,
            password=password,
            database=database
        )


        if connection.is_connected():
            print("Connected to MySQL database")

           
            cursor = connection.cursor()

            
            query = "SELECT * FROM user_details"
            cursor.execute(query)

            
            rows = cursor.fetchall()

           
            if rows:
                columns = [column[0] for column in cursor.description]
                table = PrettyTable(columns)
                table.align = 'l' 

                for row in rows:
                    table.add_row(row)

                print(table)
            else:
                print("No data found in the table.")

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")

    finally:
        
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection closed")

def search_for_user(username_user,password_user):
    try:
        connection = mysql.connector.connect(
            host=hostname,
            user=username,
            password=password,
            database=database
        )
        if connection.is_connected():
            cursor=connection.cursor(buffered=True)
            query="SELECT * FROM user_details WHERE user_name=%s AND password=%s"
            data=(username_user,password_user)
            cursor.execute(query,data)
            connection.commit()
            row=cursor.fetchone()
            if row:
                connection.close()
                print("MySQL connection closed")
                return row[4]
            
            else:
                connection.close()
                print("MySQL connection closed")
                return 0
    
    except mysql.connector.Error as e:
            print(f"Error: {e}")
            return 0
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection closed")
            return 0
    return 0

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',target="_self")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username_login=request.form['username']
        password_login=request.form['password']
        hashed_password_login = hashlib.sha256(password_login.encode()).hexdigest()
        a=search_for_user(username_login,hashed_password_login)
        if a==0:
            return redirect(url_for('signup'))
        else:
            return redirect(url_for('home',user_id=a))

        
    return render_template('login.html',target="_self")

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        username_user=request.form['username']
        name_user=request.form['name']
        email_user=request.form['email']
        password_user=request.form['password']
        hashed_password = hashlib.sha256(password_user.encode()).hexdigest()
        insert_data(name_user, username_user, email_user, hashed_password)
        return redirect(url_for('login'))


    return render_template('signup.html',target="_self")

@app.route('/home/user/<int:user_id>')
def home(user_id):
    return render_template('home.html',target="_self")

@app.route('/admin')
def admin():
    return render_template('admin.html',target="_self")

@app.route('/videopage')
def videopage():
    return render_template('videopage.html',    target="_self")












 
if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
