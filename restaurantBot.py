import telebot
from telebot import types
import const
import psycopg2
from config import config

bot = telebot.TeleBot(const.API_TOKEN)

def connect():
	""" Connect to the PostgreSQL database server """
	conn = None
	try:
		# read connection parameters
		params = config()

		# connect to the PostgreSQL server
		print('Connecting to the PostgreSQL database...')
		conn = psycopg2.connect(**params)

		# create a cursor
		cur = conn.cursor()

		# execute a statement
		print('PostgreSQL database version:')
		cur.execute('SELECT version()')

		# display the PostgreSQL database server version
		db_version = cur.fetchone()
		print(db_version)

		# close the communication with the PostgreSQL
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
			print('Database connection closed.')

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
         CREATE TABLE customers( id SERIAL PRIMARY KEY, user_id VARCHAR(100) NOT NULL, first_name VARCHAR(50), last_name VARCHAR(50))
        """,""" CREATE TABLE parts2 (
                part_id SERIAL PRIMARY KEY,
                part_name VARCHAR(255) NOT NULL
                )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_user(user_id, first_name, last_name):
	""" insert a new vendor into the vendors table """
	sql = """INSERT INTO customers(user_id, first_name, last_name)
             VALUES(%s, %s, %s) RETURNING id"""
	conn = None
	vendor_id = None
	try:
		# read database configuration
		params = config()
		# connect to the PostgreSQL database
		conn = psycopg2.connect(**params)
		# create a new cursor
		cur = conn.cursor()
		# execute the INSERT statement
		cur.execute(sql, (user_id, first_name, last_name))
		# get the generated id back
		vendor_id = cur.fetchone()[0]
		print(vendor_id)
		# commit the changes to the database
		conn.commit()
		# close communication with the database
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

	return vendor_id

@bot.message_handler(commands=['start'])
def send_welcome(message):
	print(message)
	connect();
	#create_tables()
	#insert_user('new_user', 'sdfsdfds', 'dasdas')

	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['help'])
def helper_handler(message):
	bot.reply_to(message, "How can I help you?")



@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling()
