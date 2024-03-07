#!/usr/bin/python3
from os import getenv
#from uuid import uuid4
from sqlalchemy import desc
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash ,check_password_hash
from datetime import datetime
from flask_session import Session
from werkzeug.utils import secure_filename
import os
from user import User
from db import session as db_session,engine
from flask import Flask, session as flask_session,render_template,request,redirect,url_for,flash,abort
from model import Base
from post import Post



app=Flask(__name__)
app.config['SECRET_KEY']="sasa"
app.config['UPLOAD_FOLDER']='test/static'
app.config['MAIL_SERVER']="smtp.gmail.com"
app.config['MAIL_PORT']=587
app.config['MAIL_USERNAME']="mugomadavid24@gmail.com"
app.config['MAIL_PASSWORD']="iajk bunu rlts alps"
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USE_SSL']=False
app.config['MAIL_DEFAULT_SENDER'] = ('Mugoma_Dev', 'mugomadavid24@gmail.com')

Mail=Mail(app)

@app.route("/")
def base():
  return render_template('base.html')

@app.route("/dashboard")
def dashboard():
   username=flask_session.get('username')
   id=flask_session.get('id')
   if username:
     flash("Logged in  successfully", 'success')
     return render_template("dash.html",username=username)

@app.route("/signup", methods=['GET','POST'])
def signup():
  if request.method=="POST":
    email=request.form.get("email")
    username=request.form.get("username")
    password=request.form.get("password")
    comrade=db_session.query(User).filter_by(email=email).first()
    if comrade:
      flash("Email already exists!",'danger')
      return redirect(url_for('signup'))
    password_hash= generate_password_hash(password)
    new_comrade=User(email=email, username=username ,password=password_hash)
    db_session.add(new_comrade)
    db_session.commit()
    db_session.close()
    flash("Registration successful!",'success')
    return redirect(url_for('login'))
  return render_template('signup.html')  

@app.route("/login",methods=['GET','POST'])
def login():
  if request.method=="POST":
  
    username=request.form['username']
    password=request.form['password']
    comrade=db_session.query(User).filter_by(username=username).first()
    if comrade and check_password_hash(comrade.password,password):
       flask_session['username']=username
       flask_session['id']=comrade.id
       return redirect(url_for('dashboard'))
  
    else: 
      flash("Invalid username or password. Please try again .","danger")

  return render_template("login.html")

@app.route('/reset_password' , methods=['GET'])
def show_reset_password_form():
  return render_template('reset_password.html')

@app.route('/reset_password', methods=['POST','GET'])
def get_reset_password_form():
  """write some logic here"""
  #write existing code here
  if request.method=='POST':
   email=request.form.get('email')
  user=db_session.query(User).filter_by(email=email).first()
  if user:
    

    user.generate_reset_token()
    db_session.commit()
    send_reset_email(user.email,user.username,user.token)

  return render_template('reset_password_email_sent.html',email=email)

def send_reset_email(email,user,token):
  reset_link=f"https://portal.mugoma.tech/update_password?token={token}"
  msg=Message('Password Reset instructions ',sender=('Mugoma_Dev','mugomadavid24@gmail.com'),recipients=[email])
  msg.body=f"Hello {user},\n\n I received a request to reset your password.Kindly click the below link to reset your password:\n\n{reset_link}.\n\nIf you didn't request a password reset, please ignore this email.\n\n Best regards ,\n Mugoma David."
  Mail.send(msg)


@app.route('/update_password', methods=['POST', 'GET'])
def update_password():
    if request.method == 'POST':
        token = request.form.get('token')
        new_password = request.form.get('new_password')

        comrade= db_session.query(User).filter_by(token=token).first()
        if comrade and comrade.is_reset_token_valid:
            comrade.password = generate_password_hash(new_password)
            comrade.token = ""
            comrade.reset_token_expiry=None
            # Use an reempty string or another value
            db_session.commit()
            db_session.close()
            
        return redirect(url_for('login'))
    else:
        token = request.args.get('token') 
        if not token:
          abort(403)
        return render_template('update_password.html', token=token)


@app.route("/logout")
def logout():
  if 'username' in flask_session:
   flask_session.pop('username',None)
  return redirect(url_for('signup'))

@app.route("/about")
def about():
 return render_template('about.html')

@app.route("/track_session")
def track_session():
  #username=flask_session.get('username')
 # user_id=flask_session.get('id')
 # if username and user_id:
  posts = db_session.query(Post).order_by(desc(Post.date_posted)).all()
  
  return render_template('track.html',posts=posts)


@app.route("/add_post", methods=['POST','GET'])
def add_post():
  if request.method=="POST":
    topic=request.form.get('topic')
    mentor=request.form.get('mentor')
    date_str=request.form.get('date_str')
    time_str=request.form.get('time_str')
    description=request.form.get('description')
    duration_str=request.form.get('duration_str')

    if "id" in flask_session:
      user_id=flask_session['id']
      new_post=Post(mentor=mentor,topic=topic,date_str=date_str,time_str=time_str,description=description,duration_str=duration_str,user_id=user_id)
      db_session.add(new_post)
      db_session.commit()
      db_session.close()
      return redirect(url_for("track_session"))
    else:
      return redirect(url_for("add_post"))
  return render_template("dash.html")


if __name__=="__main__":
 
   with app.app_context():
        Base.metadata.create_all(bind=engine)

   app.run(host="0.0.0.0",debug=True)




@app.route("/logout")
def logout():
  if 'username' in flask_session:
   flask_session.pop('username',None)
  return redirect(url_for('base'))

@app.route("/about")
def about():
 return render_template('about.html')

@app.route("/track_session")
def track_session():
  #username=flask_session.get('username')
 # user_id=flask_session.get('id')
 # if username and user_id:
  posts=db_session.query(Post).all()
  
  return render_template('track.html',posts=posts)


@app.route("/add_post", methods=['POST','GET'])
def add_post():
  if request.method=="POST":
    topic=request.form.get('topic')
    mentor=request.form.get('mentor')
    date_str=request.form.get('date_str')
    time_str=request.form.get('time_str')
    description=request.form.get('description')
    duration_str=request.form.get('duration_str')

    if "id" in flask_session:
      user_id=flask_session['id']
      new_post=Post(mentor=mentor,topic=topic,date_str=date_str,time_str=time_str,description=description,duration_str=duration_str,user_id=user_id)
      db_session.add(new_post)
      db_session.commit()
      db_session.close()
      return f"Submision send successfully."
    else:
      return f" user not found!"
  return render_template("post.html")


if __name__=="__main__":
 
   with app.app_context():
        Base.metadata.create_all(bind=engine)

   app.run(host="0.0.0.0",debug=True)

