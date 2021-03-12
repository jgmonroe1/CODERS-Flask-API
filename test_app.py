import unittest
import requests


BASE = "http://127.0.0.1:5000/"


class TestApp(unittest.TestCase):

	def test_start_up(self):
		response = requests.get(BASE)
		response_string = response.json()
		self.assertEqual(response_string[:31],"Welcome to the CODERS database!")

	def test_show_tables(self):
		response = requests.get(BASE+"/tables")
		response_list = response.json()
		self.assertEqual(type(response_list),type([1,1]))

	def test_return_table_wrong_table(self):
		response = requests.get(BASE+"/tables/not_a_table")
		response_string = response.json()
		self.assertEqual(response_string,"Table does not exist.")

	def test_return_ref_wrong_id(self):
		response = requests.get(BASE+"/tables/reference_list/wrong_id")
		response_string = response.json()
		self.assertEqual(response_string, "ID must be an integer.")

if __name__ == '__main__':
	unittest.main()