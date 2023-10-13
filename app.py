from flask import Flask, render_template, request, redirect, url_for, make_response

import pymongo
from bson.objectid import ObjectId
from pymongo import MongoClient

from db import db # we import from the db file now

app = Flask(__name__)

collection = db['users'] #how to create the collection variable

usersCollection = db['users']
postsCollection = db['posts']

@app.route('/')
def home():
    return 'Hello, World!'  # Change this to render_template once we build the CSS HTML

@app.route('/post')
def postPage():
    return render_template("postPage.html", title = "PINEAPPLE", postContent = "HELLO THIS IS THE CONNTENTNTENKWNKN")


if __name__ == "__main__":
    app.run(debug=True)
