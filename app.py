from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash, Response

import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps
from pymongo import MongoClient

from db import db # we import from the db file now

app = Flask(__name__)

app.secret_key = 'your_secret_key_here'

usersCollection = db['users']
postsCollection = db['posts']

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
    newUser = {"username":username, "password":password, "email":email, "role":userRole}
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

# @app.route('/feed', methods=['GET'])
# def feed():
#     return render_template('feed.html')

FEED_NUM_POSTS = 20
@app.route('/feed-posts', methods=['GET'])
def getFeedPosts():
    feed_posts = list(postsCollection.find({}).limit(FEED_NUM_POSTS))
    for post in feed_posts:
        vote = 0
        if 'userId' in session and 'votes' in post:
            for v in post['votes']:
                if v['userId'] == session['userId']:
                    vote = v['vote']
                    break
        if 'votes' in post:
            del post['votes']
        post['vote'] = vote
    return dumps(feed_posts)

@app.route('/vote_post/<post_id>/<vote>', methods=['POST'])
def votePost(post_id, vote):
    post = postsCollection.find_one({"_id":ObjectId(post_id)})
    if post is None:
        return Response('This post may have been deleted.', 404)
    if 'username' not in session:
        return Response('You must be logged in to vote.', 401)
    if 'votes' not in post:
        post['votes'] = []
    vote = int(vote)  # -1, 0, 1
    old_vote = 0
    old_vote_ind = -1
    for i, v in enumerate(post['votes']):
        if v['userId'] == session['userId']:
            old_vote = v['vote']
            old_vote_ind = i
            break
    score_change = vote - old_vote
    post['score'] = post.get('score', 0) + score_change
    if old_vote_ind >= 0:
        post['votes'][old_vote_ind]['vote'] = vote
    else:
        post['votes'].append({'userId': session['userId'], 'vote': vote})
    postsCollection.replace_one({"_id":ObjectId(post_id)}, post)

    # return copy
    del post['votes']
    post['vote'] = vote
    return dumps(post)

@app.route('/post/<post_id>')
def postPage(post_id):
    title = postsCollection.find_one({"_id":ObjectId(post_id)})['title']
    content = postsCollection.find_one({"_id":ObjectId(post_id)})['content']
    data = postsCollection.find_one({"_id":ObjectId(post_id)})['comments']
    user = postsCollection.find_one({"_id":ObjectId(post_id)})['user']
    return render_template("postPage.html", title = title, postContent = content, comments = data, user = user, currentUser = session['username'])

if __name__ == "__main__":
    app.run(debug=True)
