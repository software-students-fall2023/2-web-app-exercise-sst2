from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import load_dotenv
import os

import pymongo
import datetime
from bson.objectid import ObjectId
import sys
from pymongo import MongoClient

app = Flask(__name__)
# How to connect using a local mongodb
# client = MongoClient('mongodb://localhost:27017/')
# db = client['hw05']
# collection = db['reviews']
# res = collection.count_documents({})
# documents = collection.find({})

# # print(res)

# for doc in documents:
#     print(doc)

# try:

#     if db:
#         print("Pineppla")
#     else:
#         print("HEEE")

# except Exception:
#     print("HERE")

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


@app.route('/')
def home():
    return 'Hello, World!'  # Change this to render_template once we build the CSS HTML


if __name__ == "__main__":
    app.run(debug=True)
