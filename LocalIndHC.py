# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from pymongo import Connection, MongoClient
import json
import os

# conn = Connection('127.0.0.1', 27017)

app = Flask(__name__)

# the toolbar is only enabled in debug mode:
app.debug = False

Auth = []
Auth.append(0)

 # set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = os.urandom(24)

toolbar = DebugToolbarExtension(app)

@app.route ("/")
def find():
	
# 	export "MYAPP_DB_USER"='-----' and same for pass

# 	USER = os.environ.get("MYAPP_DB_USER", '')
# 	PASS = os.environ.get("MYAPP_DB_PASSWORD", '')

	USER = os.environ['MYAPP_DB_USER']
	PASS = os.environ['MYAPP_DB_PASSWORD']

	client = MongoClient('mongodb://'+USER+':'+PASS+'@ds027738.mongolab.com:27738/mongotest_dpc')
	db = client.mongotest_dpc

	dbR = db['RiverLevels']

# 	res = dbR.find({"date": {"$gt": "2014-01-17"}})
	
	res = dbR.find().sort("_id", -1).limit(1)  # get latest DB entry
	# 	res = dbR.find()

	FF = []
	GG = []
	ik = 0
	for i in res:
			for kt in i['data']:
				FF = []
				for j in range(0,len(kt)):
					YY = kt[j].replace("'","")
					FF.append(YY)
				ik+=1
				GG.append(str(FF))
		
	return render_template('LocalHeatCanv.html',title='Index', dat=GG)


# @app.route ('/login',methods=['POST', 'GET'])
# def login_post():
#      USER = {'Dan':'Test'}
#      error = None
#      if request.method == 'POST':
#      	if (request.form['email'] in USER and request.form['password'] in USER.values()):		 
#      		Auth[0] = 1
#      		return redirect('http://127.0.0.1:5000/stats')
# # 			return render_template('login.html', error = 'Good Login')
#      	else:
#      		error = 'Invalid username/password'
#      		return render_template('login.html', error=error)

	

# @app.route ("/stats")
# def find(name=None,desc2=None, stat=None, colst=None):
# 	
# 	dbn = 'TestCol'
# 	
# 	USER = os.environ.get("MYAPP_DB_USER", '')
# 	PASS = os.environ.get("MYAPP_DB_PASSWORD", '')
# 
# 	client = MongoClient('mongodb://'+USER+':'+PASS+'@ds027738.mongolab.com:27738/mongotest_dpc')
# 	db = client.mongotest_dpc
# 
# 	dbDocs = []
# 	dbstat = json.dumps(db.command("dbstats"))  # database stats - TEST
# 	colstat = json.dumps(db.command("collstats", "TestCol")) # collection stat
# 
# 	dbTest = db['TestCol']
# 
# 	res =  dbTest.find()
# 	cnt =  dbTest.count()
# 
# 	x = '<font size ="5">'+"<strong>"+"Document Number is:  " + str(cnt) +"</strong>"
# 
# 	desc = []
# 
# 	for i in dbTest.find():
# 		desc.append(' '.join(i['tags']))
# 
# 	desc2 = desc
# 
# 	y = '<br><br>'+ '<font size ="4">' +' '.join(desc)
# 	
# 	if Auth[0] == 1: 
# 		return render_template('stats.html', num=cnt, desc2=desc2, dbn=dbn, dbstat=dbstat, colstat=colstat)
# 	else:
# 		return render_template('login.html')
# 	
# 
# 
# @app.route ("/input")
# def input():
#     return render_template('input.html')




if __name__ == "__main__":
    app.run()