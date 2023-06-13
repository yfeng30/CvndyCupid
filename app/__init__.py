# coding=utf8

from flask import Flask, render_template, session, request, redirect
import sqlite3
import os #?
from db_handle import *


app = Flask(__name__)
app.app_context().push()

#for later
app.secret_key = os.urandom(32)



#i forgot difference between get/post!
#code not shamelessly repurposed from p3
@app.route('/', methods=['GET'])
def login():
    if 'username' in session: #when cookie work
    #if(False):
        return redirect('/swipe')
    return render_template('login.html') #names subject to change

@app.route('/register', methods=['GET', 'POST'])
def register():
  return render_template('register.html')

@app.route('/signup', methods=['GET', 'POST'])
def make_account():
  if check_user(request.form.get('username')): #NEED a method to verify if a username is taken
  #if(False):
    return render_template('register.html', status='Username is in use!')

  #new entry
  print(request.form.get('password'))
  print(request.form.get('password_confirm'))
  if (request.form.get('password') != request.form.get('password_confirm')):
    return render_template('register.html', status='The passwords typed are not the same!')
  print("register " + request.form.get('username') + " " + request.form.get('password'))
  create_user(request.form.get('pfp'), request.form.get('username'), request.form.get('password'), request.form.get('full_name'), request.form.get('dob'), request.form.get('contact'), request.form.get('college'), request.form.get('major'), request.form.get('bio')) #NEED method to create an entry in the table
  session['username'] = request.form['username']
  print(session['username'])
  return redirect('/swipe') #/home or /
  
#this method actually verifies whether or not the login works
@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
  #print(check_pass(request.form.get('username'), request.form.get('password')))
  #print("login " + request.form.get('username') + " " + request.form.get('password'))
  if not (check_user(request.form.get('username'))):
    return render_template('login.html', status="User doesn't exist!")
  if not (check_pass(request.form.get('username'), request.form.get('password'))): #NEED method to take in a username and password and return if that entry exists
    return render_template('login.html', status='Incorrect password!')
  session['username'] = request.form['username']
  return redirect('/swipe')

#forgot to actually allow a logout (I think it was in the site map)
@app.route('/logout')
def logout():
  session.pop('username')
  #"popped user: " + session.pop('username'))
  return redirect('/')

@app.route('/swipe', methods = ['GET', 'POST'])
def swipe():
  return render_template(
    "swipe.html",
    )
@app.route('/profile', methods = ['GET', 'POST'])
def profile():
  person = session['username']
  info = get_profile(person)
  return render_template(
    "profile.html",
    username = person,
    pfp = info['pfp'],
    full_name = info['full_name'], 
    dob = info['dob'], 
    contact = info['contact'], 
    college = info['college'], 
    major = info['major'], 
    bio = info['bio']
  )

@app.route('/matches', methods = ['GET', 'POST'])
def matches():
  return render_template("matches.html")

if __name__ == '__main__':
    app.debug = True
    app.run()