import unittest
import requests
import mysql.connector

BASE = "http://127.0.0.1:5000/"

class Tests(unittest.TestCase):
    ## Initialize the mysql cursor
    db = mysql.connector.connect(
        host='', 
        user='', 
        password='', 
        database=''
    )
    cursor = db.cursor()

    ## List of tables you can access through the api
    accessible_tables = ("generators",
                        "substations",
                        "transmission_lines",
                        "storage_batteries",
                        "interties",
                        "junctions",
                        "distribution_transfers",
                        "contribution_transfers",
                        "generation_costs",
                        "international_transfers",
                        "interprovincial_transfers",
                        "provincial_demand",
                        "intertie_all",
                        "intertie_provincial",
                        "cpi_can",
                        "references")

    def test_return_table(self):
        for table in accessible_tables:
            #Arrange
            if table == "substations":
                query = f"SELECT \
                            n.name, \
                            n.node_code, \
                            n.node_type, \
                            s.sub_type, \
                            n.owner, \
                            n.province, \
                            n.latitude, \
                            n.longitude, \
                            n.planning_region, \
                            n.sources, \
                            n.notes \
                            FROM nodes n \
                        JOIN substations s ON n.node_code = s.sub_node_code;"
            elif table == "junctions":
                query = f"SELECT * FROM nodes WHERE node_type = 'JCT';"
            elif table == "interties":
                query = f"SELECT \
                            n.name, \
                            n.node_code, \
                            n.node_type, \
                            i.intertie_type, \
                            n.owner, \
                            n.province, \
                            n.latitude, \
                            n.longitude, \
                            n.planning_region, \
                            n.sources, \
                            n.notes \
                            FROM nodes n \
                        JOIN interties i ON n.node_code = i.int_node_code;"
            else:
                query = f"SELECT * FROM {table};"
            cursor.execute(query)
            query_results = cursor.fetchall()

            #Act
            response = requests.get(BASE + table)
            response_code = response.status_code
            response_dict = response.json()

            #Assert
            ## Check the status code and return type
            self.assertEqual(response_code, 200)
            self.assertEqual(type(response_dict), dict)
            
            ## Check if the number of rows is equal
            self.assertEqual(len(response_dict), len(query_results))

            ## Check if the first row is the same
            for i,column in enumerate(response_dict[0]):
                self.assertEqual(column[1], query_results[i])
            
            ## Check if the last row is the same
            for i,column in enumerate(response_dict[-1]):
                self.assertEqual(column[1], query_results[i])

if __name__ == '__main__':
	unittest.main()