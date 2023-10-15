from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash

import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps
from pymongo import MongoClient

from db import db # we import from the db file now

app = Flask(__name__)

app.secret_key = 'your_secret_key_here'

collection = db['users'] #how to create the collection variable

usersCollection = db['users']
postsCollection = db['posts']

@app.route('/')
def home():
    isLoggedIn = 'username' in session
    return render_template('home.html', isLoggedIn = isLoggedIn)  # Change this to render_template once we build the CSS HTML

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
        session['userId'] = str(user['_id'])
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
        flash("Sign up successful! You can now login.")
        return redirect(url_for('loginPage'))
    except:
        error = "Something went wrong with creating your account. Please try again..."
        return render_template('signup.html', error = error)

@app.route('/logOut')
def logOut():
    session.pop('username', None)
    session.pop('userId', None)
    flash("You have successfully logged out!")
    return redirect(url_for('home'))

@app.route('/feed', methods=['GET'])
def feed():
    return render_template('feed.html')

FEED_NUM_POSTS = 20
@app.route('/feed-posts', methods=['GET'])
def getFeedPosts():
    return dumps(list(postsCollection.find({}).limit(FEED_NUM_POSTS)))

@app.route('/post')
def postPage():
    title = postsCollection.find_one({"_id":ObjectId('6529dee0699948aacd3a1e4c')})['title']
    content = postsCollection.find_one({"_id":ObjectId('6529dee0699948aacd3a1e4c')})['content']
    data = postsCollection.find_one({"_id":ObjectId('6529dee0699948aacd3a1e4c')})['comments']
    user = postsCollection.find_one({"_id":ObjectId('6529dee0699948aacd3a1e4c')})['user']
    return render_template("postPage.html", title = title, postContent = content, comments = data, user = user)

if __name__ == "__main__":
    app.run(debug=True)
