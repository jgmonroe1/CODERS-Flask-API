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
		response = requests.get(BASE+"/tables/generators")
		response_list = response.json()
		self.assertEqual(type(response_list),type([1,1]))

	def test_return_table_wrong_table(self):
		response = requests.get(BASE+"/tables/not_a_table")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'],'Table not recognized')

	def test_return_columns(self):
		response = requests.get(BASE+"/tables/substations/attributes")
		response_list = response.json()
		self.assertEqual(type(response_list),type([1,1]))

	def test_return_columns_junctions(self):
		response = requests.get(BASE+"/tables/junctions/attributes")
		response_list = response.json()
		self.assertEqual(type(response_list),type([1,1]))

	def test_return_columns_wrong_table(self):
		response = requests.get(BASE+"/tables/not_a_table/attributes")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'],'Table not recognized')
	#return_ref is quite difficult to test as we cant garentee that given ref_id 
	#is in the system. Therefor testing the response from a good or bad ID is difficult
	#should try find a better way
	def test_return_ref_not_int(self):
		response = requests.get(BASE+"/tables/reference_list/not_an_int")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 400)
		self.assertEqual(response_dict['message'],'Key must be an integer')

	def test_return_ref_zero(self):
		response = requests.get(BASE+"/tables/reference_list/0")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 400)
		self.assertEqual(response_dict['message'],'Key must be a positive integer')

	def test_return_ref_negative(self):
		response = requests.get(BASE+"/tables/reference_list/-123")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 400)
		self.assertEqual(response_dict['message'],'Key must be a positive integer')

	def test_return_based_on_prov(self):
		response = requests.get(BASE+"/tables/substations/NB")
		response_list = response.json()
		self.assertEqual(type(response_list),type([1,1]))

	def test_return_based_on_prov_wrong_table(self):
		response = requests.get(BASE+"/tables/not_a_table/NB")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'],'Table not recognized')

	def test_return_based_on_prov_wrong_prov(self):
		response = requests.get(BASE+"/tables/generators/XX")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 400)
		self.assertEqual(response_dict['message'],'Invalid province')

	def test_return_international_hourly_transfers_wrong_input(self):
		response = requests.get(BASE+"/tables/international_transfers/2022_XX_YY")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 400)
		self.assertEqual(response_dict['message'],'Invalid province, state, year combination')

	def test_return_interprovincial_hourly_transfer(self):
		response = requests.get(BASE+"/tables/interprovincial_transfers/2022_XX_YY")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 400)
		self.assertEqual(response_dict['message'],'Invalid province, province, year combination')

	def test_return_provincial_hourly_demand(self):
		response = requests.get(BASE+"/tables/provincial_demand/2022_XX")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 400)
		self.assertEqual(response_dict['message'],'Invalid province and year combination')


if __name__ == '__main__':
	unittest.main()
