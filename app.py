from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import load_dotenv
import os

import pymongo
import datetime
from bson.objectid import ObjectId
import sys

app = Flask(__name__)

load_dotenv()  # take environment variables from .env.

# turn on debugging if in development mode
if os.getenv('FLASK_ENV', 'development') == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode

# connect to the database
cxn = pymongo.MongoClient(os.getenv('MONGO_URI'), serverSelectionTimeoutMS=5000)
try:
    # verify the connection works by pinging the database
    cxn.admin.command('ping') # The ping command is cheap and does not require auth.
    db = cxn[os.getenv('MONGO_DBNAME')] # store a reference to the database
    print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!
except Exception as e:
    # the ping command failed, so the connection is not available.
    print(' *', "Failed to connect to MongoDB at", os.getenv('MONGO_URI'))
    print('Database connection error:', e) # debug

@app.route('/')
def home():
    return 'Hello, World!' #Change this to render_template once we build the CSS HTML

if __name__ == "__main__":
    app.run(debug=True)