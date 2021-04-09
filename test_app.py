import unittest
import requests

BASE = "http://127.0.0.1:5000"


class TestApp(unittest.TestCase):

	def test_start_up(self):
		response = requests.get(BASE)
		response_string = response.json()
		self.assertEqual(response_string[:31],"Welcome to the CODERS database!")
	
	def test_return_docs_wrong_spelling(self):
		response = requests.get(BASE + "/ap/doc")
		response_string = response.json()
		response_code = response.status_code
		self.assertEqual(response_code, 404)
		self.assertEqual(response_string['message'], 'Table not recognized')
		
	def test_return_filters_wrong_spelling(self):
		response = requests.get(BASE + "/fiters")
		response_string = response.json()
		response_code = response.status_code
		self.assertEqual(response_code, 404)
		self.assertEqual(response_string['message'], 'Table not recognized')

	def test_return_filters(self):
		response = requests.get(BASE + '/filters')
		response_string = response.json()
		response_code = response.status_code
		self.assertEqual(response_code, 200)
		self.assertEqual(response_string[:34], 'Province: substations, generators,')

	def test_show_tables(self):
		response = requests.get(BASE+"/tables")
		response_list = response.json()
		self.assertEqual(type(response_list),type([1,1]))
	
	def test_return_table_wrong_spelling(self):
		response = requests.get(BASE + "/talbes")
		response_message = response.json()
		response_code = response.status_code
		self.assertEqual(response_code, 404)
		self.assertEqual(response_message['message'], 'Table not recognized')

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

	def test_return_columns_wrong_spelling(self):
		response = requests.get(BASE + "/junctions/atributes")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'], '/junctions/atributes not recognized')

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
		response = requests.get(BASE+"/references?key=not_an_int")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'],'Key must be a positive integer')

	def test_return_ref_zero(self):
		response = requests.get(BASE+"/references?key=0")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'],'Key must be a positive integer')

	def test_return_ref_negative(self):
		response = requests.get(BASE+"/references?key=-123")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'],'Key must be a positive integer')
	def test_return_ref_not_in_db(self):
		response = requests.get(BASE + "/references?key=200000000")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'], 'Key was not associated with any reference')

	def test_return_based_on_prov(self):
		response = requests.get(BASE+"/substations?province=NB")
		response_list = response.json()
		self.assertEqual(type(response_list),list)

	def test_return_based_on_prov_wrong_table(self):
		response = requests.get(BASE+"/not_a_table?province=NB")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'],'Table not recognized')

	def test_return_based_on_prov_wrong_prov(self):
		response = requests.get(BASE+"/generators?province=XX")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'],'No results found')

	def test_return_international_hourly_transfers_wrong_input(self):
		response = requests.get(BASE+"/international_transfers?year=2022&province=XX&us_region=YY")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'],'No results found')

	def test_return_interprovincial_hourly_transfer(self):
		response = requests.get(BASE+"/interprovincial_transfers?year=2022&province1=XX&province2=YY")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'],'No results found')

	def test_return_provincial_hourly_demand(self):
		response = requests.get(BASE+"/provincial_demand?year=2022&province=XX")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'],'No results found')

	def test_return_generator_type_wrong_type(self):
		response = requests.get(BASE+"/generators?province=NL&type=foo")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'], 'Invalid generator type')

	def test_return_generator_type_wrong_province(self):
		response = requests.get(BASE+"/generators?province=FOO&type=hydro_daily")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'], 'No hydro_daily generators found in FOO')

	def test_return_generator_type_no_results(self):
		response = requests.get(BASE + "/generators?province=AB&type=hydro_monthly")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'], 'No hydro_monthly generators found in AB')

	## TRY BREAK THE CODE
	##=======================

	## Requests the international transfers without a US state
	def test_international_transfers_no_state(self):
		response = requests.get(BASE+"/international_transfers?year=2018&province=AB")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'], 'No US region provided')

	def test_international_transfers_no_province(self):
		response = requests.get(BASE+"/international_transfers?year=2018&us_region=Montana")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'], 'No province provided')

	def test_international_transfers_no_year(self):
		response = requests.get(BASE+"/international_transfers?province=2018&us_region=Montana")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'], 'No year provided')

	def test_interprovincial_transfers_no_year(self):
		response = requests.get(BASE+"/interprovincial_transfers?province_1=AB&province_2=BC")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'], 'No year provided')

	def test_interprovincial_transfers_one_province(self):
		response = requests.get(BASE+"/interprovincial_transfers?year=2018&province_1=AB")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'], 'Did not provide two provinces')

	def test_interprovincial_transfers_no_provinces(self):
		response = requests.get(BASE+"/interprovincial_transfers?year=2018")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'], 'Did not provide two provinces')

	def test_provincial_demand_no_year(self):
		response = requests.get(BASE + "/provincial_demand?province=AB")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'], 'No year provided')
	
	def test_provincial_demand_no_prov(self):
		response = requests.get(BASE + "/provincial_demand?year=2018")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'], 'No province provided')

	def test_gen_type_no_province(self):
		response = requests.get(BASE + "/generators?type=coal")
		response_code = response.status_code
		response_dict = response.json()
		self.assertEqual(response_code, 404)
		self.assertEqual(response_dict['message'], 'No province provided')
if __name__ == '__main__':
	unittest.main()