from flask import Flask, request, jsonify, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
import shortuuid
import validators
from config import Config
from bson.objectid import ObjectId

app = Flask(__name__)
app.config.from_object(Config)

client = MongoClient(app.config['MONGO_URI'])
db = client[app.config['DB_NAME']]
urls_collection = db['urls']
