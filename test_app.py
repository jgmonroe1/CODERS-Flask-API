import unittest
import requests


BASE = "http://127.0.0.1:5000"


class TestApp(unittest.TestCase):

	def test_start_up(self):
		response = requests.get(BASE)
		response_string = response.json()
		self.assertEqual(response_string[:31],"Welcome to the CODERS database!")

	def test_show_tables(self):
		response = requests.get(BASE+"/tables")
		response_list = response.json()
		self.assertEqual(type(response_list),type([1,1]))

	def test_return_table(self):
		response = requests.get(BASE+"/generators")
		response_list = response.json()
		self.assertEqual(type(response_list),type([1,1]))

	def test_return_table_wrong_table(self):
		response = requests.get(BASE+"/not_a_table")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'],'Table not recognized')

	def test_return_columns(self):
		response = requests.get(BASE+"/substations/attributes")
		response_list = response.json()
		self.assertEqual(type(response_list),type([1,1]))

	def test_return_columns_junctions(self):
		response = requests.get(BASE+"/junctions/attributes")
		response_list = response.json()
		self.assertEqual(type(response_list),type([1,1]))

	def test_return_columns_wrong_table(self):
		response = requests.get(BASE+"/not_a_table/attributes")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'],'Table not recognized')
	#return_ref is quite difficult to test as we cant garentee that given ref_id 
	#is in the system. Therefor testing the response from a good or bad ID is difficult
	#should try find a better way
	def test_return_ref_not_int(self):
		response = requests.get(BASE+"/reference_list/key=not_an_int")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 400)
		self.assertEqual(response_dict['message'],'Key must be an integer')

	def test_return_ref_zero(self):
		response = requests.get(BASE+"/reference_list/key=0")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 400)
		self.assertEqual(response_dict['message'],'Key must be a positive integer')

	def test_return_ref_negative(self):
		response = requests.get(BASE+"/reference_list/key=-123")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 400)
		self.assertEqual(response_dict['message'],'Key must be a positive integer')

	def test_return_based_on_prov(self):
		response = requests.get(BASE+"/substations/province=NB")
		response_list = response.json()
		self.assertEqual(type(response_list),type([1,1]))

	def test_return_based_on_prov_wrong_table(self):
		response = requests.get(BASE+"/not_a_table/province=NB")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'],'Table not recognized')

	def test_return_based_on_prov_wrong_prov(self):
		response = requests.get(BASE+"/generators/province=XX")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 200)
		self.assertEqual(response_dict['message'],'No results found')

	def test_return_international_hourly_transfers_wrong_input(self):
		response = requests.get(BASE+"/international_transfers/year=2022&province=XX&us_region=YY")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 200)
		self.assertEqual(response_dict['message'],'No results found')

	def test_return_interprovincial_hourly_transfer(self):
		response = requests.get(BASE+"/interprovincial_transfers/year=2022&province1=XX&province2=YY")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 200)
		self.assertEqual(response_dict['message'],'No results found')

	def test_return_provincial_hourly_demand(self):
		response = requests.get(BASE+"/provincial_demand/year=2022&province=XX")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 200)
		self.assertEqual(response_dict['message'],'No results found')


if __name__ == '__main__':
	unittest.main()