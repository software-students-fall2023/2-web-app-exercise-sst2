from flask import Flask, render_template, request, redirect, url_for, make_response, session
from dotenv import load_dotenv
import os

import pymongo
import datetime
from bson.objectid import ObjectId
import sys
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
# How to connect using a local mongodb
# client = MongoClient('mongodb://localhost:27017/')
# db = client['hw05']
# collection = db['reviews']
# res = collection.count_documents({})
# documents = collection.find({})

# # print(res)

# for doc in documents:
#     print(doc)

load_dotenv()  # take environment variables from .env.

# turn on debugging if in development mode
if os.getenv('FLASK_ENV', 'development') == 'development':
    # turn on debugging, if in development
    app.debug = True  # debug mnode

# connect to the database
cxn = pymongo.MongoClient(os.getenv('MONGO_URI'),
                          serverSelectionTimeoutMS=5000)

try:
    # verify the connection works by pinging the database
    # The ping command is cheap and does not require auth.
    cxn.admin.command('ping')
    db = cxn[os.getenv('MONGO_DBNAME')]  # store a reference to the database
    # if we get here, the connection worked!
    print(' *', 'Connected to MongoDB!')
except Exception as e:
    # the ping command failed, so the connection is not available.
    print(' *', "Failed to connect to MongoDB at", os.getenv('MONGO_URI'))
    print('Database connection error:', e)  # debug


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
