from flask import Flask, render_template,redirect,request,flash, session,send_file,url_for,send_from_directory
# from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps 
import pymysql.cursors
import os
import secrets
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.debug = True



db_config = {
    "host": "localhost",
    "user": "impapztr_impactmass",
    "password": "Impactmass@123",
    "database": "impapztr_impactmass",
    "cursorclass": pymysql.cursors.DictCursor  # Optional: Use a dictionary cursor for easier data handling
}

# db_config = {
#     "host": "localhost",
#     "user": "root",
#     "password": "",
#     "database": "trial",
# }
app.secret_key = 'U8kIj1vDxOy66r4Q9mE8zW2qVzPpJwBbT5lY7xZaRdU0u3sT6oC4gH9nM2gD3kK'



def generate_random_filename(filename):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(filename)
    new_filename = random_hex + ext
    return new_filename



UPLOAD_FOLDER = 'dynamic/blogs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def con():
    return pymysql.connect(**db_config)

@app.errorhandler(500)
def internal_server_error(e):
    return "Internal Server Error", 500

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            # flash("You need to login first")
            return redirect(url_for('login'))

    return wrap


if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

# sql quarry for database to create
db='''CREATE TABLE IF NOT EXISTS user(
    id INT PRIMARY KEY AUTO_INCREMENT,
    fname VARCHAR(100),
    lname VARCHAR(100),
    email VARCHAR(100),
    phone INT,
    date VARCHAR(100),
    gender VARCHAR(10),
    username VARCHAR(200),
    password VARCHAR(200)

    )'''


comment='''CREATE TABLE IF NOT EXISTS comment(
com_id INT PRIMARY KEY AUTO_INCREMENT,
com_token VARCHAR(100),
user_id VARCHAR(100),
blog_id VARCHAR(100),
comment VARCHAR(500),
date VARCHAR(100),
time VARCHAR(100),
lk VARCHAR(100)

)'''

 

blog='''CREATE TABLE IF NOT EXISTS blog(
blog_id INT PRIMARY KEY AUTO_INCREMENT,
title VARCHAR(100),
shortcontect VARCHAR(100),
content VARCHAR(10000),
date VARCHAR(100),
time VARCHAR(100),
image VARCHAR(200),
imagename VARCHAR(100),
writer VARCHAR(100)

)'''




feedback = '''CREATE TABLE IF NOT EXISTS feedback(
feed_id INT PRIMARY KEY AUTO_INCREMENT,
email VARCHAR(100),
feedback VARCHAR(100)
)'''


cur = con()
curs = con()


# Create a cursor to execute SQL queries
with cur.cursor() as curso:
    try:
        curso.execute(feedback)
        curso.execute(comment)
        curs.commit()
    except Exception as e:
        # Handle the exception, print an error message, or take necessary actions
        print("Error occurred:", str(e))

with cur.cursor() as cursor:
    try:
        # Execute the CREATE TABLE statement
        cursor.execute(db)
        cursor.execute(feedback)
        cursor.execute(blog)
        cursor.execute(comment)
        

        # Commit the changes (only needed if you have modifications to the database)
        cur.commit()

    except Exception as e:
        # Handle the exception, print an error message, or take necessary actions
        print("Error occurred:", str(e))

# Close the connection



@app.route('/')
def index():
    
    return render_template('index.html')



from flask import abort


# for hosting server

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please provide both username and password.', 'error')
            return redirect(url_for('login'))

        # Attempt to retrieve user data from the database
        try:
            with con().cursor() as cursor:
                cursor.execute("SELECT * FROM user WHERE username = %s", [username])
                user_data = cursor.fetchone()
        except Exception as e:
            flash('Error occurred while fetching user data.', 'error')
            print("Error occurred:", str(e))
            return redirect(url_for('login'))

        if not user_data:
            flash('Invalid credentials or User does not exist/registered.', 'error')
            return redirect(url_for('signup'))

        # Verify the password
        stored_password = user_data.get('password')
        if sha256_crypt.verify(password, stored_password):
            session["logged_in"] = True
            session["userId"] = user_data.get('id')
            return redirect(url_for('blogs'))
        else:
            flash('Wrong password.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


# for vs code and local server 

# @app.route('/login' ,methods=['POST','GET'])
# def login():
#      if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         cur = con()
#         with cur.cursor() as cur:
#          cur.execute("SELECT * FROM user WHERE username = %s", [username])
#         # cur.execute("SELECT * FROM user WHERE password = %s", [password])
#         res = cur.fetchone()
#         if res:
#             pwd = res[8]
#             if sha256_crypt.verify(password, pwd):
#                 session["logged_in"]=True
#                 session["userId"] = res[0]
#                 # flash('Logged in')
#                 return redirect(url_for('blogs'))
#             else:
#                 print('Wrong password')
#                 flash('Invalid credentials or User does not exist/registered')
#                 return redirect(url_for('signup'))
#         cur.close()
#      return render_template('login.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/signup', methods=['POST','GET'])
def signup():
        if request.method == 'POST':
            fname = request.form['fname']
            lname = request.form['lname']
            email = request.form['email']
            phone = request.form['phone']
            date = request.form['date']
            gender = request.form['gender']
            username = request.form['username']
            password = sha256_crypt.encrypt(str(request.form['password'])) 
            curs = con()
            with curs.cursor() as cur:
             cur.execute("INSERT INTO user (fname, lname,email,phone,date,gender, username, password) VALUES(%s,%s,%s,%s,%s,%s, %s, %s)", [
                        fname, lname,email,phone,date,gender,username, password])
             curs.commit()
            #  cur.close()
            flash('Thank you for registering with MindRing')
            return redirect(url_for('login'))
        return render_template('signup.html')


@app.route('/home')
def home():
    return render_template('home.html')



@app.route('/blogs')
def blogs():
        curs = con()
        try:
         with curs.cursor() as cursor:
            sql = '''SELECT * FROM blog '''
            cursor.execute(sql)

            data = cursor.fetchall()
        #  data.reverse()
        finally:
         curs.close()
         text_response = "\n".join([str(row) for row in data])
        
         return render_template('blog.html',blog=data)
        

@app.route('/blog/readmore/<val>' , methods=['POST','GET'])
def blogcontent(val):
    #  userid = session['userId']
     t = request.args.get('val')
     curs = con()
     try:
         with curs.cursor() as cursor:
            sql = '''SELECT * FROM blog WHERE blog_id=%s'''
            # comment = '''SELECT * FROM comment WHERE blog_id =%s'''
            user =  '''
                SELECT comment.*, user.fname,lname
                FROM comment
                JOIN user ON comment.user_id = user.id
                WHERE comment.blog_id = %s
            '''
            cursor.execute(sql,[val])
            

            data = cursor.fetchall() 
            # cursor.execute(comment,[val])
            # com = cursor.fetchall() 

            cursor.execute(user,[val])
            userdata = cursor.fetchall() 


        #  data.reverse()
     finally:
         curs.close()

     return render_template('blogcontent.html',blog=data,user=userdata )



@app.route('/comment',methods=['POST','GET'])
@login_required
def comment():
    userid = session['userId']
    if request.method == 'POST':
     blogid = request.form['blogid']
     comid = request.form['comid']
     comment = request.form['comment']
     date = request.form['date']
     time = request.form['time']
    curs = con()
    with curs.cursor() as cur:
             cur.execute("INSERT INTO comment (com_token, user_id,blog_id,comment,date,time) VALUES(%s,%s,%s,%s,%s,%s)", [
                        comid, userid,blogid,comment,date,time])
             curs.commit()


    return redirect(url_for('blogcontent', val=blogid))


 

@app.route('/blogpost' , methods=['POST','GET'])
def blogpost():
    # try:
    #          with curss.cursor() as curs:
    #             bp='''INSERT INTO blog (title,shortcontect,content,date,image) VALUES (%s,%s,%s,%s,%s,%s)'''



    if request.method == "POST":
        title = request.form['title']
        shortcontect = request.form['shortcontect']
        content  = request.form['content']
        date = request.form['date']
        image = request.files['image']
        # file = image.filename
        if image:
         fname = secure_filename(image.filename)
        filename  = generate_random_filename(fname)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename ))
        # imagename = request.form['imagename']
        # write = request.form['write']
        curs = con()
        try:
         with curs.cursor() as cursor:
            sql = '''INSERT INTO blog (title, shortcontect, content, date, image) 
                     VALUES (%s, %s, %s, %s, %s)'''
            cursor.execute(sql, (title, shortcontect, content, date, filename))
            curs.commit()  # Commit the changes
            return redirect(url_for('blogs'))
        finally:
         curs.close()

       
        
        
    return render_template('test.html')
    
    
@app.route('/feedback',methods=['POST','GET'])
def feedback():
    if request.method == 'POST':
        email = request.form['email']
        feedback = request.form['feedback']
        curs = con()
        with curs.cursor() as cur:
            cur.execute("INSERT INTO feedback (email, feedback) VALUES(%s,%s)", [email,feedback])
            curs.commit()
            #  cur.close()
            flash('Thank you for Your Valueable Feedback')
            return redirect(url_for('index'))

    return render_template('feedback.html')

if __name__ == '__main__':
    app.run()
#  hst='192.168.29.26'
# prt='5000'
# app.run(host=hst,port=prt,debug=True)    