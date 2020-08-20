import mysql.connector

from dotenv import load_dotenv
import os

load_dotenv()

db_tweets = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv('PASSWORD_ROOT_DB')
)

mycursor = db_tweets.cursor()

mycursor.execute("CREATE DATABASE " + os.getenv('NAME_DATABASE'))


