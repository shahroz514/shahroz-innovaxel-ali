from flask import Flask, request, jsonify, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
import shortuuid
import validators
from config import Config
from bson.objectid import ObjectId
