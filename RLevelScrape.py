from __future__ import division

import pymongo
from pymongo import MongoClient
import base64
import requests
import nltk
# from lxml import html
import datetime as dt
import pandas as pd
import numpy as np
from time import sleep
import os


Err = []
Hour =  dt.datetime.now().hour
Sched = [6,9,12,14,16,18,20,22]

if Hour in Sched:


	attempts = 15

	# prox = ['216.155.156.67','64.120.29.99','208.52.180.213	','216.59.131.70']


	for attempt in xrange(attempts):
		print attempt
	
		try:
			HC2 = []
			HCID = []
			HCLoc = []
			UpdateT = []
			D = {}
			Risk = []
			HeatCanv = []

	# 		t = pd.read_csv('/Users/danielcollins/anaconda/envs/RiversEE/code/StationsLatLon2.csv')
		
			t = pd.read_csv('StationsLatLon2.csv')
		
			Rid = t.icol(0).astype('int')
			ix2 = Rid.size
			ix = 0
			cnt = 0

			HeatLst = []
			Location = []
	
			for tx in range(0, ix2):
	# 		for tx in range(0, 1):

			
	# 			np.random.shuffle(prox)
	# 			proxies = {"http":"http://"+prox[1]}

	# 			if tx%10==0:
	# 				print "Using Proxy:" 
	# 			else:
	# 				print ''
				
				tx2 = Rid[tx]
				URL = 'http://www.environment-agency.gov.uk/homeandleisure/floods/riverlevels/120717.aspx?stationId='+str(tx2)
	
				page = requests.get(URL)
	# 			sleep(0.05)
	
	# 			tree = html.fromstring(page.text)

				A = page.text
				Summ = page.text.rfind('Summary')
				TrimP = A[Summ:]
				Summ_end = TrimP.find('</div>')

				Summary = A[Summ:Summ+Summ_end]

				Sum_E = str(nltk.clean_html(Summary))

				SS = Sum_E.replace('\r\n', '')
				SS2 = SS


			# 	print SS2

				Station = '"'+nltk.clean_html(str(A[A.rfind('<h1>'):A.rfind('</h1>')]))+'"'
				if Station == 'Station not active':
					Station = 'Station_not_active'+str(cnt)
					Location.append(Station)
					cnt+=1
				else:
					Location.append(Station)
	
				print 50* '-'
				print Station
	
				print "%i of %i" %(tx, ix2)
				print 50*'-'
	
				W = SS2.split()

				Levels = []
				Date = []
				Time = []


				for i in W:
					try:
						Levels.append(float(i))
					except:
						pass

				for i in W:
					try:
						Date.append(dt.datetime.strptime(i, "%d/%m/%Y."))
					except:
						pass

				Time = SS2[SS2.find(':')-2:SS2.find(':')+3]

				if len(Levels) > 0 and SS2.find('invalid')<0:
		
					Update = Time + ' ' + dt.datetime.strftime(Date[0], "%d/%m/%Y")
					Up = dt.datetime.strptime(Update, "%H:%M %d/%m/%Y")

					Up = '"'+dt.datetime.strftime(Up, "%Y-%m-%d %H:%M")+'"'
				
					UpdateT.append(Up)

	
	
	
					li = ['CurrentL', 'LowTypical', 'HighTypical', 'HighestRecord']

					d = {}

					try:
						Date[1] = dt.datetime.strftime(Date[1], "%Y-%m-%d")
					except:
						Date.append(np.NaN)

					d['Update'] = Up
				# 	d['RecDate'] = Date[1]
	
					d['CurrentL'] = Levels[0]
	
					if SS2.find('highest')>=0:
						d['HighestRec'] = max(Levels)
					else:
						d['HighestRec'] = np.NaN
	
					if SS2.find('typical')>=0:
						d['LowTypical'] = Levels[1]
						d['HighTypical'] = Levels[2]
					else:
						d['LowTypical'] = np.NaN
						d['HighTypical'] = np.NaN
	
					d['Lat'] = t['Lat'][tx]
					d['Lon'] = t['Lon'][tx]	
					try:
						a1 = d['CurrentL']/d['HighTypical'] 
						if np.isnan(a1) == True:
							d['risk'] = 0
						else:
							d['risk'] = float(np.round(a1,3)*10)
					except:
						d['risk'] = 0

					D[Station] = d
	# 		basic list of values for heatcanvas /////////////////
				
				
					HeatLst.append({'lat':d['Lat'],'lon':d['Lon'],'value':d['risk']})
		
					ix+=1
		
					Risk.append(float(np.round(d['risk'],2)))
				
	# 				HeatCanv.append([d['Lat'],d['Lon'],float(np.round(d['risk'],2)),Up,Station,tx2,d['CurrentL']])
					HeatCanv.append([str(d['Lat']),str(d['Lon']),str(d['risk']),Up,Station,str(tx2),str(d['CurrentL'])])

					HC2.append([tx2,Station,d['Lat'],d['Lon'],float(np.round(d['risk'],2))])
					HCLoc.append(Station)
					HCID.append(tx2)
				
				
				else:
					D[Station] = 'N/A'
					Err.append(tx2)
					ix+=1

			testData = {'max': max(Risk), 'data':HeatLst}

		except Exception, e:
			print e
		else:
			break
	
	# //////////////////////////// Mongo upload //////////////////////////////////////////////

	print Err
	
	if len(HeatCanv) > 1900:

		USER = os.environ.get("MYAPP_DB_USER", '')
		PASS = os.environ.get("MYAPP_DB_PASSWORD", '')
		client = MongoClient('mongodb://'+USER+':'+PASS+'@ds027738.mongolab.com:27738/mongotest_dpc')
		db = client.mongotest_dpc # Specify database to connect to	

		postx = db.RiverLevels
		TS = dt.datetime.now()
		dte = dt.datetime.strftime(TS, "%Y-%m-%d %H:%M")

		post2 = {}
		post2['data'] = HeatCanv
		post2['date'] = dte
		post2['stations'] = len(HeatCanv)

		 
		 
		postx.insert(post2)
	else:
		print "Scraper Failed After Several Attempts"

else:
	print "Not Scheduled To Run"
		