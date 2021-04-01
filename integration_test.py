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
        # for table in accessible_tables:
        #     response = requests.get(BASE + table)
        #     response_code = response.status_code
        #     response_dict = response.json()
        #     self.assertEqual(response_code, 200)
        #     if table == "substations":
        #         query = f"SELECT \
        #                     n.name, \
        #                     n.node_code, \
        #                     n.node_type, \
        #                     s.sub_type, \
        #                     n.owner, \
        #                     n.province, \
        #                     n.latitude, \
        #                     n.longitude, \
        #                     n.planning_region, \
        #                     n.sources, \
        #                     n.notes \
        #                     FROM nodes n \
        #                 JOIN substations s ON n.node_code = s.sub_node_code;"
        #     elif table == "junctions":
        #         query = f"SELECT * FROM nodes WHERE node_type = 'JCT';"
        #     elif table == "interties":
        #         query = f"SELECT \
        #                     n.name, \
        #                     n.node_code, \
        #                     n.node_type, \
        #                     i.intertie_type, \
        #                     n.owner, \
        #                     n.province, \
        #                     n.latitude, \
        #                     n.longitude, \
        #                     n.planning_region, \
        #                     n.sources, \
        #                     n.notes \
        #                     FROM nodes n \
        #                 JOIN interties i ON n.node_code = i.int_node_code;"

        #     cursor.execute(query)
        #     for 
if __name__ == '__main__':
	unittest.main()