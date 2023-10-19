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
    feed_posts.sort(key=lambda p: p['_id'].generation_time, reverse=True)
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
    post = postsCollection.find_one({"_id":ObjectId(post_id)})
    user = post['user']
    comment_ids = post.get("comments", [])    
    data = commentsCollection.find({"_id": {"$in": comment_ids}})
    return render_template("postPage.html", comments = data, sessionName = session['username'], post = post, post_id = post_id)

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
    return render_template("createPost.html", username = session['username'])

@app.route('/create', methods = ['POST'])
def createPost():
    username = session['username']
    user_input = request.form.get('postContent')
    title = request.form.get('title')

    if user_input and title:
        try:
            inserted_id = postsCollection.insert_one({'title': title, 'content': user_input, 'comments':[], 'user': username}).inserted_id
            usersCollection.update_one({"username": username}, {"$push": {"posts":inserted_id}})
            return redirect("/")
        except:
            flash("An error occurred while creating the post. Please try again.")
            return redirect(url_for('create'))
    else:
        return redirect(url_for('create'))
    
@app.route('/deletepost', methods = ['POST'])
def deletePost():
    post_id = request.form.get('post_id')
    comment_ids = postsCollection.find_one({'_id': ObjectId(post_id)})['comments']
    user = postsCollection.find_one({'_id': ObjectId(post_id)})['user']
    postsCollection.delete_one({"_id": ObjectId(post_id)}) 
    usersCollection.update_one({'username':user}, {'$pull' : {"posts": ObjectId(post_id)}}) 
    commentsCollection.delete_many({"_id":{"$in":comment_ids}})
    updateUsers = usersCollection.find({"comments":{"$in":comment_ids}})

    for user in updateUsers:
        user["comments"] = [comment_id for comment_id in user["comments"] if comment_id not in comment_ids]
        usersCollection.update_one({"username": user["username"]}, {"$set": {"comments": user["comments"]}})
    return redirect('/')

@app.route('/deletecomment', methods = ['POST'])
def deleteComment():
    comment_id = request.form.get('comment_id')
    post_id = request.form.get('post_id')
    user = commentsCollection.find_one({'_id': ObjectId(comment_id)})['user']

    postsCollection.update_one({'_id':ObjectId(post_id)}, {'$pull' : {"comments": ObjectId(comment_id)}}) 
    commentsCollection.delete_one({"_id": ObjectId(comment_id)}) 
    usersCollection.update_one({'username':user}, {'$pull' : {"comments": ObjectId(comment_id)}}) 
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
