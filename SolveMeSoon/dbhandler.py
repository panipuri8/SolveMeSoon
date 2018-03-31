import pymysql
import requests

SERVER_NAME = "localhost"
DB_USERNAME = "root"
DB_PASSWORD = "password"
DB_NAME = "mysql"

USERS_TABLE = "cp_todo_list_users"
PROBLEMS_TABLE = "cp_todo_list_problems"

SOME_ERROR = 1001

ADDED_NEW_USER = 5001
USERNAME_ALREADY_EXISTS = 5002

VALID_LOGIN = 6001
INVALID_USERNAME = 6002
WRONG_PASSWORD = 6003

EMPTY_TODO_LIST = 7001
SUCCESSFUL_TODO_LIST = 7002

PROBLEM_ADDED = 8001
PROBLEM_ALREADY_EXISTS = 8002
INVALID_PROBLEM  = 8003
NOT_CONNECTED_TO_INTERNET = 8004

PROBLEMS_DELETED = 9001


def add_new_user(username,password,email):
	try:
		db = pymysql.connect(SERVER_NAME , DB_USERNAME , DB_PASSWORD ,DB_NAME)
		cursor = db.cursor()
		sql = "select * from cp_todo_list_users where username=%s"
		cursor.execute(sql, (username))
		data = cursor.fetchall()
		if(len(data)>0):
			return USERNAME_ALREADY_EXISTS
		sql = "insert into cp_todo_list_users(username,password,email_id) values(%s,%s,%s)"
		cursor.execute(sql, (username,password,email))
		db.commit()
		return ADDED_NEW_USER
	except Exception as e:
		print("EXCEPTION IN DBHANDLER",e.__class__.__name__)
		print(e)
		db.rollback()
		return SOME_ERROR


def login(username,password):
	try:
		db = pymysql.connect(SERVER_NAME , DB_USERNAME , DB_PASSWORD ,DB_NAME)
		cursor = db.cursor()
		sql = "select * from cp_todo_list_users where username=%s"
		cursor.execute(sql, (username))
		data = cursor.fetchall()
		if(len(data)<=0):
			return INVALID_USERNAME
		if(len(data)>1):
			return SOME_ERROR
		actual_password = data[0][1] #contains the password
		if(actual_password == password):
			return VALID_LOGIN
		else:
			return WRONG_PASSWORD
	except Exception as e:
		print("EXCEPTION IN DBHANDLER",e.__class__.__name__)
		print(e)
		return SOME_ERROR

def get_problems(username):
	try:
		db = pymysql.connect(SERVER_NAME , DB_USERNAME , DB_PASSWORD ,DB_NAME)
		cursor = db.cursor()
		sql = "select problemid from cp_todo_list_problems as one inner join cp_todo_list_users as two on one.username =%s and one.username = two.username"
		cursor.execute(sql, (username))
		data = cursor.fetchall()
		if(len(data)<=0):
			return EMPTY_TODO_LIST
		myDict = [{"problemid":row[0]} for row in data]
		return myDict
	except Exception as e:
		print("EXCEPTION IN DBHANDLER",e.__class__.__name__)
		print(e)
		return SOME_ERROR

def add_problem(username, problemid):
	try:
		r = requests.head("https://www.codechef.com/problems/" + problemid)
		# print(r.status_code)
		if(r.status_code != 200):
			print("Invalid problem here")
			return INVALID_PROBLEM
		db = pymysql.connect(SERVER_NAME , DB_USERNAME , DB_PASSWORD ,DB_NAME)
		cursor = db.cursor()
		sql = "select * from cp_todo_list_problems where username=%s and problemid=%s"
		cursor.execute(sql,(username,problemid))
		data = cursor.fetchall()
		if(len(data)>0):
			return PROBLEM_ALREADY_EXISTS
		sql = "insert into cp_todo_list_problems(problemid,username) values(%s,%s)"
		cursor.execute(sql,(problemid,username))
		db.commit()
		return PROBLEM_ADDED
	except requests.ConnectionError:
		return NOT_CONNECTED_TO_INTERNET
	except Exception as e:
		print("EXCEPTION IN DBHANDLER",e.__class__.__name__)
		print(e)
		db.rollback()
		return SOME_ERROR

def delete_problem(username, list_of_problems):
	try :
		print("In database")
		db = pymysql.connect(SERVER_NAME , DB_USERNAME , DB_PASSWORD ,DB_NAME)
		cursor = db.cursor()
		for problem in list_of_problems:
			sql = "delete from cp_todo_list_problems where username=%s and problemid=%s"
			cursor.execute(sql,(username,problem))
		db.commit()
		return PROBLEMS_DELETED
	except Exception as e:
		print("EXCEPTION IN DBHANDLER",e.__class__.__name__)
		print(e)
		db.rollback()
		return SOME_ERROR

if(__name__ == '__main__'):
	x = add_problem('panipuri8' , 'RANDOM')
	print(x)