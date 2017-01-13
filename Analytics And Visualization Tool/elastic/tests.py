from django.test import TestCase
import json
# Create your tests here.

class TestAPI(TestCase):

	# def test_elastic(self):
	# 	response = self.client.get('/elastic/api/elastic/?pathInput=%s&indexInput=%s' %('/home/jk/Jk/python/DjangoProject/New/djangoprojectfinal/MutualFunds.csv','jk'))
	# 	res = (response.content).decode('utf-8')
	# 	res_dict = json.loads(res)
	# 	status = res_dict.get('status')
	# 	self.assertEquals('success',status)

	# def test_deleteInput(self):
	# 	response = self.client.get('/elastic/api/deleteInput/?deleteInput=%s' %('abcd6'))
	# 	res = (response.content).decode('utf-8')
	# 	res_dict = json.loads(res)
	# 	status = res_dict.get('status')
	# 	self.assertEquals('success',status)

	# def test_oneByOneInput(self):
	# 	response = self.client.get('/elastic/api/oneByOneInput/?indexNamePath=%s&jsonObj=%s' %('abcd10','{"mfname":"testMfname","aum":2000,"ret_3yrs":3000,"ret_2yrs":8000,"ret_1yr":2000,"ret_5yrs":2500}'))
	# 	res = (response.content).decode('utf-8')
	# 	res_dict = json.loads(res)
	# 	status = res_dict.get('status')
	# 	self.assertEquals('success',status)

	def test_retrieve(self):
		response = self.client.get('/elastic/api/retrieve/?tablename=%s&indexname=%s' %('MobileDB','jkmob3'))
		res = (response.content).decode('utf-8')
		res_dict = json.loads(res)
		status = res_dict.get('status')
		self.assertEquals('success',status)