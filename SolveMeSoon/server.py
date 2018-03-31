from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
import dbhandler

app = Flask(__name__,static_url_path="")

@app.route("/signup",methods=['POST'])
def signup():
	try:
		data = request.get_json(force=True)
		result = dbhandler.add_new_user(data['uname'],data['pass'],data['mail'])
		if(result == dbhandler.USERNAME_ALREADY_EXISTS):
			return jsonify({"Error":"Username already exists"})
		elif(result == dbhandler.ADDED_NEW_USER):
			return jsonify({"Success":"Added"})
		else:
			raise Exception
	except Exception as e:
		return jsonify({"Error":"Something went wrong"})

@app.route("/login",methods=['POST'])
def login():
	try:
		data = request.get_json(force=True)
		result = dbhandler.login(data['uname'],data['pass'])
		if(result == dbhandler.VALID_LOGIN):
			return jsonify({"Success":"Added"})
		elif(result == dbhandler.INVALID_USERNAME):
			return jsonify({"Error":"Username does not exist"})
		elif(result == dbhandler.WRONG_PASSWORD):
			return jsonify({"Error":"Wrong Password"})
	except Exception as e:
		print(e)
		return jsonify({"Error":"Something went wrong"})

@app.route("/problems" , methods=['POST'])
def get_problems():
	try:
		data = request.get_json(force=True)
		result = dbhandler.get_problems(data['uname'])
		if(result == dbhandler.EMPTY_TODO_LIST):
			return jsonify({"Empty":"Empty ToDo List"})
		else:
			return jsonify(result)
	except Exception as e:
		print(e)
		return jsonify({"Error":"Something went wrong"})

@app.route("/addproblem" , methods=['POST'])
def add_problem():
	try:
		data = request.get_json(force=True)
		result = dbhandler.add_problem(data['uname'],data['problemid'])
		if(result == dbhandler.PROBLEM_ALREADY_EXISTS):
			print("SERVER.py" , "ALREADY EXISTS")
			return jsonify({"Problem":"Problem already exists in your todo list!"})
		elif(result == dbhandler.INVALID_PROBLEM):
			print("SERVER.py" , "DOES NOT EXIST")
			return jsonify({"Problem":"Invalid Problem Code"})
		elif(result == dbhandler.NOT_CONNECTED_TO_INTERNET):
			print("SERVER.py" , "NO INTERNET")
			return jsonify({"Problem":"Connect to the internet while adding problems!"})
		elif(result == dbhandler.PROBLEM_ADDED):
			print("SERVER.py" , "PROBLEM ADDED BECAUSE IT WAS NEW !")
			return jsonify({"Success":"Added"})
	except Exception as e:
		print(e)
		return jsonify({"Error":"Something went wrong"})

@app.route("/delete", methods=['POST'])
def delete_problems():
	try:
		data = request.get_json(force=True)
		username = data["username"]
		pcodes = data["pcodes"]
		result = dbhandler.delete_problem(username,pcodes)
		if(result == dbhandler.PROBLEMS_DELETED):
			return jsonify({"Success":"Deleted"})
		else:
			return jsonify({"Error" : "Some error occured in the database"})
	except Exception as e:
		print(e)
		return jsonify({"Error":"Something went wrong"})


if(__name__ == '__main__'):
	app.run(debug = True)
