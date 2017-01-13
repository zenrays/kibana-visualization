from django.shortcuts import render,redirect
from django.http import HttpResponse	
from django.views.generic import View	
from django.template import Context, loader
import json
import csv
from django.db.models import Q
from elasticsearch import Elasticsearch
from .models import MobileDB
import sqlite3

# Create your views here.

def func_hello(request):
	''' This function is just for testing purposes '''
	res = 'hello world response using function view jk'
	return HttpResponse(res)



def indexUI(request):
	''' This function is for linking the url of the index.html page which accepts the path of the csv file '''
	template = loader.get_template("index.html")
	return HttpResponse(template.render())


def deleteIndex(request):
	''' This function is for the linking of the deleteIndex.html page which deletes a index from Elastic Search'''
	template = loader.get_template("deleteIndex.html")
	return HttpResponse(template.render())


def oneByOne(request):
	''' This function is for the linking of the obeByOne.html page which push a single json object onto an existing index in Elastic Search'''
	template = loader.get_template("oneByOne.html")
	return HttpResponse(template.render())


def dbin(request):
	''' This function is for the linking of the dbInput.html page which adds data onto the Database'''
	template = loader.get_template("dbInput.html")
	return HttpResponse(template.render())


def retrievehtml(request):
	''' This function is for the linking of the retrieve.html page which retrieves data from database and push it onto Elastic Search'''
	template = loader.get_template("retrieve.html")
	return HttpResponse(template.render())


def elastic(request):
	''' This function accepts the url and index name from the index.html file and parse the data and push it onto ES.'''
	status = 'failure'
	FILE_URL = str(request.GET['pathInput'])
	indexName = str(request.GET['indexInput'])
	
	ES_HOST = {
	     "host" : "localhost", 
	     "port" : 9200
	}
	
	es = Elasticsearch(hosts = [ES_HOST])
	csvfile= open(FILE_URL,'r')
	csv_reader = csv.reader(csvfile, dialect=csv.excel_tab)
	i=1
	result = {}
	fieldName=[]
	res = {}
	# this block recognizes the column names in the csv file and make a tuple containing 
	# just the column names.

	try:
		for row in csv_reader:
		    if row:
		        row_str = row[0];
		        row_arr = row_str.split(',');
		        for f in range(0,len(row_arr)):
		            fieldName.append(row_arr[f])
		        break
	except Exception as e:
		result[status] = e
		return HttpResponse(json.dumps(result))

	# This block parses the csv file and push the data onto ES according to the
	# given index name.
	z=1
	try:
		for row in csv_reader:
			my_dict = {}
			if row:
				row_str = row[0]
				row_arr = row_str.split(',')
				for f in range(0,len(row_arr)):
					try:
						row_arr[f]= float(row_arr[f])
						my_dict[fieldName[f]] = (row_arr[f])

					except Exception as e:
						row_arr[f] = row_arr[f].strip()
						for i in range(0,len(row_arr[f])):
							if(row_arr[f][i].isspace()):
								row_arr[f] = row_arr[f].replace(row_arr[f][i],'_')
							else:
								row_arr[f] = row_arr[f]
						my_dict[fieldName[f]] = (row_arr[f])
				
				es.index(index=indexName, doc_type=indexName, body=(my_dict))

				es.indices.refresh(index=indexName)
				
	except Exception as e:
		result[status] = e
		return HttpResponse(json.dumps(result))

	status = 'success'

	if(status == 'failure'):
		result[status] = 'Something wrong'
		return HttpResponse(json.dumps(result))
	elif(status == 'success'):
		# return redirect('http://localhost:5601/app/kibana#/settings/')
		result['status'] = 'success'
		return HttpResponse(json.dumps(result))
		
		


def deleteInput(request):
	''' This function is for deleting an existing index from the Elasticsearch '''
	indexName = request.GET['deleteInput']
	
	ES_HOST = {
	     "host" : "localhost", 
	     "port" : 9200
	}
	
	result ={}
	status = 'failure'

	es = Elasticsearch(hosts = [ES_HOST])
	
	# this block checks if the given index exists. if it exists then it deletes it from the ES database.

	try:
		if(es.indices.exists(index=indexName)):
			es.indices.delete(index=indexName)
			z = indexName + " deleted from Elasticsearch"	

			status = 'Success'

			result[status] = z
			result['status'] = 'success'
			return HttpResponse(json.dumps(result))
		else:
			z = indexName+" doesn't exists.Couldn't be deleted"
			result[status] = z
			result['status'] = 'failure'

			return HttpResponse(json.dumps(result))

	except Exception as e:
		result[status] = e
		return HttpResponse(json.dumps(result))



def oneByOneInput(request):
	''' This function is for getting one json object from user and pushing onto an existing index in Elasticsearch'''
	
	indexName = request.GET['indexNamePath']
	obj = str(request.GET['jsonObj'])

	res={}
	status='failure'

	ES_HOST = {
		"host":"localhost",
		"port":9200
	}

	f=1

	# This block checks first if an index exists then push it onto ES.
	try:
		es =Elasticsearch(hosts =[ES_HOST])
		
		if(es.indices.exists(index=indexName)):
			jsonObj = json.loads(obj)
			es.index(index=indexName,body=obj,doc_type=indexName)
			es.indices.refresh(index=indexName)

			status = 'Successfully pushed data onto ES'
			res[status] = status
			res['status'] = 'success'
			return HttpResponse(json.dumps(res))

		else:
			res[status] = "index doesn't exists"
			return HttpResponse(json.dumps(res))

	except Exception as e:
		res[status] = e
		return HttpResponse(json.dumps(res))



def addingToDb(request):
	''' This function is for accepting the Table name and contents of MobileDB class and add it to the data base'''
	
	tbn = str(request.GET['tbName'])
	name = request.GET['prName']
	brand = request.GET['brName']
	cam = int(request.GET['camera'])
	ram = int(request.GET['ram'])
	mem = int(request.GET['memory'])
	battery = int(request.GET['battery'])
	price = int(request.GET['price'])
	
	try:
		tbn+='()'
		ob = eval(tbn)
		ob.name = name
		ob.brand = brand
		ob.camera = cam
		ob.ram = ram
		ob.memory = mem
		ob.battery = battery
		ob.price = price
		ob.save()

	except Exception as e:
		return HttpResponse(e)

	res = {'status':'success'}
	return HttpResponse(json.dumps(res))
	

def retrieve(request):
		''' This function is for retrieving data from database and pushing it onto ElasticSearch according to the index name given'''
	
		res = {}
		tbName = request.GET['tablename']
		indexName = request.GET['indexname']
		db = sqlite3.connect('./db.sqlite3')
		
		
		tbName=tbName.lower()
		exe = 'select * from elastic_'
		exe+=tbName
		
		db.row_factory = sqlite3.Row
		c = db.cursor()
		c.execute(exe)
		r = c.fetchone()

		tup = r.keys()
		exe = "SELECT "

		for i in range(0,len(tup)):
			if(i == (len(tup)-1)):
				exe+=(tup[i])
			else:
				if(tup[i]!='id'):
					exe+=(tup[i]+",")

		exe += (" from elastic_"+tbName )
		
		ES_HOST = {
	     "host" : "localhost", 
	     "port" : 9200
		}

		es = Elasticsearch(hosts = [ES_HOST])
		cursor = db.execute(exe)

		try:
			for row in cursor:
			   	my_dict = {}

			   	for n in range(0,len(tup)-1):
			   		try:
			   			z = float(row[n])
			   			my_dict[tup[n+1]] = z

			   		except Exception as e:
			   			z = row[n].strip()
			   			for i in range(0,len(z)):
			   				if(z[i].isspace()):
			   					z = z.replace(z[i],'_')
			   				else:
			   					z = z

			   			my_dict[tup[n+1]] = z


			   	es.index(index=indexName, doc_type=indexName, body=my_dict,ignore=[400,404])

			es.indices.refresh(index=indexName)
			res['status'] = 'success'
		except Exception as e:
	 		res["Error"] = e
	 		return HttpResponse(json.dumps(res))

		# return redirect('http://localhost:5601/app/kibana#/settings/')
		return HttpResponse(json.dumps(res))