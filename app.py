from flask import Flask, render_template, request, redirect, url_for, make_response, session

import pymongo
from bson.objectid import ObjectId
from pymongo import MongoClient

from db import db # we import from the db file now

app = Flask(__name__)

app.secret_key = 'your_secret_key_here'

collection = db['users'] #how to create the collection variable

usersCollection = db['users']
postsCollection = db['posts']

@app.route('/')
def home():
    return render_template('home.html')  # Change this to render_template once we build the CSS HTML

@app.route('/login', methods=['GET'])
def loginPage():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def loginProcess():
    username = request.form.get('username')
    password = request.form.get('password')
    user = usersCollection.find_one({'username': username})
    if user and user['password'] == password:
        session['username'] = user['username']
        return redirect(url_for('home'))
    else:
        error = "Invalid password or username"
        return render_template('login.html',error=error)
    
@app.route('/signUp', methods=['GET'])
def signUpPage():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUpProcess():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    confirmPassword = request.form.get('confirmPassword')

    if password != confirmPassword:
        error = "Passwords do not match"
        return render_template('signup.html', error = error)
    
    user = usersCollection.find_one({'username': username})

    if user:
        error = "This username already exists"
        return render_template('signup.html', error = error)
    newUser = {"username":username, "password":password, "email":email}
    try:
        usersCollection.insert_one(newUser)
        return redirect(url_for('loginPage', signup="success"))
    except:
        error = "Something went wrong with creating your account. Please try again..."
        return render_template('signup.html', error = error)



if __name__ == "__main__":
    app.run(debug=True)
