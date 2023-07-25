#!/usr/bin/python3
from os import getenv
from datetime import datetime
from flask import Flask ,render_template,request,redirect,url_for
from db import session
from  model import Item
from tent import Product


app=Flask(__name__)

@app.route("/")
def base():
   return render_template("base.html")

@app.route("/products")
def products():
  users=session.query(Product).all()
  return render_template("tent.html", users=users)

@app.route("/access")
def try_to():
  users=session.query(Item).all()
  return render_template("postem.html", me=users)

@app.route("/item/<int:n>" ,methods=['GET'] )
def show_id(n):
  user=session.query(Product).filter(Product.id==n).first()
  if not user:
    return "not found ",404
  return render_template("post.html",user=user)

@app.route("/show/<int:b>/try", methods=['POST'])
def me(b):
  if request.method=="POST":
   email=request.form.get('email')
   username=request.form.get('username')
  
   user=Item(username=username,email=email)
   user.created_at=datetime.now()
   session.rollback()
   session.add(user)
   session.commit()
   session.close()
    
  return f"Your choice was sent successfully!"



if __name__=="__main__":
 app.run(host="0.0.0.0",debug=True)

