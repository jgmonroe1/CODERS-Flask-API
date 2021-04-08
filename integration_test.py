import unittest
import requests
import mysql.connector
import decimal 

BASE = "http://127.0.0.1:5000/"

class Tests(unittest.TestCase):
    ## Initialize the mysql cursor
    db = mysql.connector.connect(
        host='localhost', 
        user='root', 
        password='', 
        database='coders_draft'
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
                        "reference_list")

    def send_query(self, query):
        cur = self.db.cursor()
        try:
            cur.execute(query)
            result = cur.fetchall()
            return list(result)
        except:
            print("issue with sql query")

    def test_return_table(self):
        for table in self.accessible_tables:
            #print("return_table table:"+table)
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

            query_results = self.send_query(query)


            #Act
            response = requests.get(BASE + table)
            response_code = response.status_code
            response_list = response.json()

            #Assert
            ## Check the status code and return type
            self.assertEqual(response_code, 200)
            self.assertEqual(type(response_list), list)
            
            ## Check if the number of rows is equal
            self.assertEqual(len(response_list), len(query_results))

            ## Check if the first row is the same
            for i,column in enumerate(response_list[0]):
                self.assertEqual(column[1], query_results[i])
            
            ## Check if the last row is the same
            for i,column in enumerate(response_list[-1]):
                self.assertEqual(column[1], query_results[i])

    def test_return_columns(self):
        for table in self.accessible_tables:
            #print("return_columns table:"+table)
            #Arrange
            #query db for expected results
            db_columns = []
            if table == 'substations':
                db_columns = ["name", 
                                "node_code", 
                                "node_type",
                                "substation_type", 
                                "owner", 
                                "province", 
                                "latitude", 
                                "longitude", 
                                "planning_region", 
                                "sources", 
                                "notes"]
            elif table == 'interties':
                db_columns = ["name", 
                                "node_code", 
                                "node_type",
                                "intertie_type", 
                                "owner", 
                                "province", 
                                "latitude", 
                                "longitude", 
                                "planning_region", 
                                "sources", 
                                "notes"]
            elif table == 'junctions':
                db_columns = ["name", 
                                "node_code", 
                                "node_type", 
                                "owner", 
                                "province", 
                                "latitude", 
                                "longitude", 
                                "planning_region", 
                                "sources", 
                                "notes"]
            else:
                # print("Table="+table+" is using query")   
                query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' ORDER BY ORDINAL_POSITION"
                results = self.send_query(query)
                if results == 0:
                    return 0
                for columns in results:
                    db_columns.append(columns[0])

            #Act
            #invoke API and collect results
            response = requests.get(BASE + table + "/attributes")
            response_code = response.status_code
            response_list = response.json()

            #Assert
            ## Check the status code and return type
            self.assertEqual(response_code, 200)
            self.assertEqual(type(response_list), list)
            
            ## Check if the number of rows is equal
            self.assertEqual(len(response_list), len(db_columns))

            ## Check if the first row is the same
            # print(response_list)
            # print("========")
            # print(db_columns)
            self.assertEqual(response_list[1], db_columns[1])
            
            ## Check if the last row is the same
            self.assertEqual(response_list[-1], db_columns[-1])

    def test_return_ref_w_good_id(self):
        #Arrange
        ref_id = 1
        query = f"SELECT * FROM reference_list WHERE id = {ref_id}"
        db_result = self.send_query(query)

        #Act
        response = requests.get(BASE + "references?key=" + str(ref_id))
        response_code = response.status_code
        response_list = response.json() 
        response_row = response_list[0].values() 
  
        #Assert
        self.assertEqual(response_code, 200)
        self.assertEqual(type(response_list), list)
        self.assertEqual(len(response_list), len(db_result))
        for i,column in enumerate(response_row):
            self.assertEqual(column, db_result[0][i])

    def test_return_based_on_province(self):
        #Arrange
        province = 'AB'
        for table in self.accessible_tables:
            if table in  ("distribution_transfers",
                            "contribution_transfers",
                            "generation_costs",
                            "international_transfers",
                            "interprovincial_transfers",
                            "provincial_demand",
                            "intertie_all",
                            "intertie_provincial",
                            "cpi_can",
                            "reference_list"):
                continue

            if table == "interties":
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
                            JOIN interties i ON n.node_code = i.int_node_code \
                            WHERE n.province = '{province}';"
            ## Query for substations joined on nodes
            elif table == "substations":
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
                            JOIN substations s ON n.node_code = s.sub_node_code \
                            WHERE n.province = '{province}';"
            elif table == "junctions":
                query = f"SELECT * FROM nodes WHERE node_type = 'JCT' AND province = '{province}';"
            else:
                query = f"SELECT * FROM {table} WHERE province = '{province}';"       

            #ACT 
            db_result = self.send_query(query)
            response = requests.get(BASE + f"{table}?province={province}")
            response_code = response.status_code
            response_list = response.json()
            ##AB contains no interties
            if table == 'interties': continue
            response_first_row = response_list[0]
            response_first_row = response_first_row.values()
            response_last_row = response_list[-1].values()
            
            #Assert
            self.assertEqual(response_code, 200)
            self.assertEqual(type(response_list), list)
            for i,column in enumerate(response_first_row):
                if type(db_result[0][i]) == decimal.Decimal:
                    db_result[0] = list(db_result[0])
                    db_result[0][i] = float(db_result[0][i])
                self.assertEqual(column, db_result[0][i])

            for i,column in enumerate(response_last_row):
                if type(db_result[-1][i]) == decimal.Decimal:
                    db_result[-1] = list(db_result[-1])
                    db_result[-1][i] = float(db_result[-1][i])
                self.assertEqual(column, db_result[-1][i])

    def return_international_hourly_transfers(self):
        ##Arrange
        province = 'AB'
        us_region = 'US-Montana'
        year = 2018
        query = f"SELECT * FROM international_transfers WHERE local_time LIKE '2018%'AND province = '{province}' and us_state = '{us_region}';"

        #Act
        db_result = self.send_query(query)
        response = requests.get(BASE + f"international_transfers?year={year}&province={province}&us_region={US-Montana}")
        response_code = response.status_code
        response_list = response.json()
        response_reow = response_list[0].values()

        #Assert
        self.assertEqual(response_code, 200)
        self.assertEqual(type(response_list),list)
        self.assertEqual(len(response_list), len(db_result))
        for i,column in enumerate(response_row):
            self.assertEqual(column,db_result[0][i])

    def return_interprovincial_hourly_transfers(self):
        ##Arrange
        province1 = 'BC'
        province2 = 'AB-AESO'
        year = 2018
        query = f"SELECT * FROM international_transfers WHERE local_time LIKE '{year}%'AND province_1 = '{province1}' and province_2 = '{province2}';"

        #Act
        db_result = self.send_query(query)
        response = requests.get(BASE + f"interprovincial_transfers?year={year}&province1={province1}&province2={province2}")
        response_code = response.status_code
        response_list = response.json()
        response_reow = response_list[0].values()

        #Assert
        self.assertEqual(response_code, 200)
        self.assertEqual(type(response_list),list)
        self.assertEqual(len(response_list), len(db_result))
        for i,column in enumerate(response_row):
            self.assertEqual(column,db_result[0][i])

    def return_provincial_hourly_demand(self):
        ##Arrange
        province = 'AB'
        year = 2018
        query = f"SELECT * FROM international_transfers WHERE local_time LIKE '{year}%' AND province_1 = '{province1}';"

        #Act
        db_result = self.send_query(query)
        response = requests.get(BASE + f"interprovincial_transfers?year={year}&province1={province1}&province2={province2}")
        response_code = response.status_code
        response_list = response.json()
        response_reow = response_list[0].values()

        #Assert
        self.assertEqual(response_code, 200)
        self.assertEqual(type(response_list),list)
        self.assertEqual(len(response_list), len(db_result))
        for i,column in enumerate(response_row):
            self.assertEqual(column,db_result[0][i])
if __name__ == '__main__':
	unittest.main()