import os

from flask import Flask
from routes import routes
from pymongo import MongoClient
from dotenv import load_dotenv
from commonLibs.initialiseLogging import InitialiseLogging
from commonLibs.globalVariables import GlobalVariables

def createApp():
    app = Flask(__name__)
    app.register_blueprint(routes.pages)
    load_dotenv()
    client = MongoClient(os.environ.get('MONGODB_URI'))
    app.db = client.get_database(os.environ.get("DATABASE_NAME"))
    InitialiseLogging().setupLogging()
    GlobalVariables.LOGGER.info("Habit Tracker")
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT")),debug=True)

# if __name__ == "__main__":
#     createApp()