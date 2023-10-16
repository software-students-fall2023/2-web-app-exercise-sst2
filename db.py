from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import load_dotenv
import os

import pymongo
import datetime
from bson.objectid import ObjectId
import sys
from pymongo import MongoClient

#We now use this file to connect to the database. add from db import db at the top of your file 

cxn = None
db = None

def connect():
    global cxn, db
    if cxn is not None:
        return
    load_dotenv()  # take environment variables from .env.

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
        return db
    
    except Exception as e:
        # the ping command failed, so the connection is not available.
        print(' *', "Failed to connect to MongoDB at", os.getenv('MONGO_URI'))
        print('Database connection error:', e)  # debug
        return None


connect()