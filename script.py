#lancer le serveur sql : sudo systemctl start mariadb

import tweepy

import mysql.connector

from dotenv import load_dotenv
import os

#chargement des variables d'environnements
load_dotenv()
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

#connexion à l'API Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#connexion à la database
db_tweets = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv('PASSWORD_ROOT_DB'),
)
mycursor = db_tweets.cursor()


def get_id_and_content_tweets_of_an_user(screen_name):
    #on lui donne à manger un screen_name
    user = api.get_user(screen_name=screen_name)
    les_ids = []
    les_contents = []
    for status in tweepy.Cursor(api.user_timeline, id=user.id, tweet_mode='extended', count=200).items():
        if status._json['id'] is None or status._json['full_text'] is None: #pour s'assurer que les deux listes ont la même longueur ; la clé est full_text car j'ai précisé tweet_mode=extended dans la requête, sinon on  utiliserait 'text'
            continue
        les_ids.append(status._json['id'])
        text = status._json['full_text']
        #on purge le texte des ' : on les double:
        if "'" in text:
            text = text.replace("'", "''")
        #on purge le texte des méchants emojis qui font tout planter
        les_contents.append(text)
    return les_ids, les_contents



def create_and_fill_new_table(name_table, screen_name):
    mycursor.execute('USE {};'.format(os.getenv('NAME_DATABASE')))
    mycursor.execute('CREATE TABLE IF NOT EXISTS {} (id BIGINT, content VARCHAR(1000)) DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;'.format(name_table))
    les_ids, les_contents = get_id_and_content_tweets_of_an_user(screen_name)
    for i in range(len(les_ids)):
        print("INSERT INTO {} (id, content) VALUES ('{}', '{}');".format(name_table, les_ids[i], les_contents[i]))
        #on gère les smileys:
        try:
            mycursor.execute("INSERT INTO {} (id, content) VALUES ('{}', '{}');".format(name_table, les_ids[i], les_contents[i]))
        except mysql.connector.errors.DataError:
            print("c'est de la merde LES EMOJIS TWITTER")
            
            #TODO, pour le moment pas géré
            pass


    


create_and_fill_new_table('trump', 'realdonaldtrump')




