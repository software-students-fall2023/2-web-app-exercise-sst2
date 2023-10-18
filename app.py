from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash

import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps
from pymongo import MongoClient

from db import db # we import from the db file now

app = Flask(__name__)

app.secret_key = 'your_secret_key_here'

usersCollection = db['users']
postsCollection = db['posts']
commentsCollection = db['comments']

# user_id = usersCollection.find({"username":session['username']})

@app.route('/')
def home():
    isLoggedIn = 'username' in session
    if isLoggedIn is False:
        return render_template('home.html')
    return render_template('feed.html', username=session['username'])  # Change this to render_template once we build the CSS HTML

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
    
@app.route('/signup', methods=['GET'])
def signUpPage():
    return render_template('signup.html')

@app.route('/signup',methods=['POST'])
def signUpProcess():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    confirmPassword = request.form.get('confirmPassword')
    userRole = "user"

    if password != confirmPassword:
        error = "Passwords do not match"
        return render_template('signup.html', error = error)
    
    user = usersCollection.find_one({'username': username})

    if user:
        error = "This username already exists"
        return render_template('signup.html', error = error)
    newUser = {"username":username, "password":password, "email":email,"comments":[], "posts":[], "role":userRole}
    try:
        usersCollection.insert_one(newUser)
        flash("Sign up successful! You can now login.")
        return redirect(url_for('loginPage'))
    except:
        error = "Something went wrong with creating your account. Please try again..."
        return render_template('signup.html', error = error)

@app.route('/logout')
def logOut():
    session.pop('username', None)
    session.pop('userId', None)
    flash("You have successfully logged out!")
    return redirect(url_for('home'))

@app.route('/feed-posts', methods=['GET'])
def getFeedPosts():
    FEED_NUM_POSTS = 20
    return dumps(list(postsCollection.find({}).limit(FEED_NUM_POSTS)))

@app.route('/post/<post_id>')
def postPage(post_id):
    print(post_id)
    post = postsCollection.find_one({"_id":ObjectId(post_id)})

    title = post['title']
    content = post['content']
    user = post['user']
    comment_ids = post.get("comments", [])    
    data = commentsCollection.find({"_id": {"$in": comment_ids}})
    return render_template("postPage.html", title = title, postContent = content, comments = data, user = user, post = post, currentUser = session['username'], username=session['username'], post_id = post_id)

@app.route('/profile/<profile_name>/comments')
def profilePageComments(profile_name):
    print(profile_name)
    comment_ids = usersCollection.find_one({"username":profile_name})['comments']
    comments = commentsCollection.find({"_id": {"$in": comment_ids}})

    return render_template("profileComment.html", comments = comments, profile_name = profile_name)

@app.route('/profile/<profile_name>/posts')
def profilePagePosts(profile_name):
    post_ids = usersCollection.find_one({"username":profile_name})['posts']
    posts = postsCollection.find({"_id": {"$in": post_ids}})
    return render_template("profilePost.html", posts=posts, profile_name = profile_name)

@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form.get('user_input')
    post_id = request.form.get('post_id')
    username = session['username']
    if user_input:
        inserted_id = commentsCollection.insert_one({'text': user_input, 'user': username}).inserted_id
        postsCollection.update_one({"_id":ObjectId(post_id)}, {"$push": {"comments": inserted_id}})
        usersCollection.update_one({"username":username}, {"$push": {"comments": inserted_id}})
        return redirect('/')
    
@app.route('/create')
def create():
    return render_template("createPost.html")

@app.route('/create', methods = ['POST'])
def createPost():
    username = session['username']
    user_input = request.form.get('user_input')
    title = request.form.get('title')
    if user_input:
        inserted_id = postsCollection.insert_one({'title': title, 'content': user_input, 'comments':[], 'user': username}).inserted_id
        usersCollection.update_one({"username": username}, {"$push": {"posts":inserted_id}})
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
