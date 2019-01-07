from flask import Flask
from flask_pymongo import PyMongo


class DatabaseConnection:
    def __init__(self):
        app = Flask(__name__)
        app.config["MONGO_URI"] = 'mongodb://localhost:27017/UBB_App'
        self.mongo_connection = PyMongo(app)
        app.run()

    def connect(self):
        return self.mongo_connection