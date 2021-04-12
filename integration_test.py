import unittest
import requests
import mysql.connector
import decimal 
import datetime

BASE = "http://127.0.0.1:5000/"

class Tests(unittest.TestCase):
    ## Initialize the mysql cursor
    db = mysql.connector.connect(
        host='localhost', 
        user='root', 
        password='Databecrazy#1978', 
        database='coders_draft'
    )
    cursor = db.cursor()

    ## List of tables you can access through the api
    # accessible_tables = ("generators",
    #                     "substations",
    #                     "transmission_lines",
    #                     "storage_batteries",
    #                     "interties",
    #                     "junctions",
    #                     "distribution_transfers",
    #                     "contribution_transfers",
    #                     "generation_costs",
    #                     "international_transfers",
    #                     "interprovincial_transfers",
    #                     "provincial_demand",
    #                     "interface_capacity",
    #                     "cpi_can",
    #                     "references"
    #                     )
    accessible_tables = ("generators",
                        "substations",
                        "transmission_lines",
                        "interties",
                        "junctions",
                        "generation_costs",
                        "international_transfers",
                        "interprovincial_transfers",
                        "transfer_capacity_copper",
                        "interface_capacity",
                        "references"
                        )

    def send_query(self, query):
        cur = self.db.cursor()
        try:
            cur.execute(query)
            result = cur.fetchall()
            return list(result)
        except:
            print("issue with sql query")

    def test_return_table(self):
        #set variables to test 
        international_transfers_test_year = 2019
        international_transfers_test_prov = "AB"
        international_transfers_test_state = "US-Montana"
        interprovincial_transfers_test_year = 2019
        interprovincial_transfers_test_prov_1 = "AB"
        interprovincial_transfers_test_prov_2 = "SK"
        #loop through each table 
        for table in self.accessible_tables:
            #Arrange
            #some tables require query modifications
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
            elif table == "international_transfers":
                query = f"SELECT * FROM international_transfers \
                            WHERE province = '{international_transfers_test_prov}' \
                            AND us_state = '{international_transfers_test_state}' \
                            AND (local_time LIKE '{international_transfers_test_year}%' \
                            OR (local_time LIKE '{int(international_transfers_test_year) + 1}%' \
                            AND annual_hour_ending = 8760));"
            elif table == "interprovincial_transfers":
                query = f"SELECT * FROM interprovincial_transfers \
                            WHERE province_1 = '{interprovincial_transfers_test_prov_1}' \
                            AND province_2 = '{interprovincial_transfers_test_prov_2}' \
                            AND (local_time LIKE '{interprovincial_transfers_test_year}%' \
                            OR (local_time LIKE '{int(interprovincial_transfers_test_year) + 1}%' \
                            AND annual_hour_ending = 8760));"            
            else:
                #references table is named reference_list in db but we changed it to be more readible
                if table == "references":
                    table = "reference_list"
                query = f"SELECT * FROM {table};"
            #after creating query send it off to db
            db_result = self.send_query(query)
            #change reference_list back to references for API call
            if table == "reference_list":
                    table = "references"    
            #Act
            #some tables need special API call
            if table == "international_transfers":
                request = BASE + table + f"?year={international_transfers_test_year}&province={international_transfers_test_prov}&us_region={international_transfers_test_state}"
            elif table == "interprovincial_transfers":
                request = BASE + table + f"?year={interprovincial_transfers_test_year}&province1={interprovincial_transfers_test_prov_1}&province2={interprovincial_transfers_test_prov_2}"
            else:
                request = BASE + table
            #invoke API and collect results
            response = requests.get(request)
            response_code = response.status_code
            response_list = response.json()

            #Assert
            ## Check the status code and return type
            self.assertEqual(response_code, 200)
            self.assertEqual(type(response_list), list)
            
            ## Check if the number of rows is equal
            self.assertEqual(len(response_list), len(db_result))
            
            ## Check if the first row is the same
            for i,column in enumerate(response_list[0].values()):
                if type(db_result[0][i]) == decimal.Decimal:
                    db_result[0] = list(db_result[0])
                    db_result[0][i] = float(db_result[0][i])
                if type(db_result[0][i]) == datetime.datetime:
                    db_result[0] = list(db_result[0])
                    db_result[0][i] = str(db_result[0][i])
                self.assertEqual(column, db_result[0][i])
            
            ## Check if the last row is the same
            for i,column in enumerate(response_list[-1].values()):
                if type(db_result[-1][i]) == decimal.Decimal:
                    db_result[-1] = list(db_result[-1])
                    db_result[-1][i] = float(db_result[-1][i])
                if type(db_result[-1][i]) == datetime.datetime:
                    db_result[-1] = list(db_result[-1])
                    db_result[-1][i] = str(db_result[-1][i])
                self.assertEqual(column, db_result[-1][i])

    def test_return_columns(self):
        for table in self.accessible_tables:
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
                if table == "references":
                    table = "reference_list" 
                query = f"SELECT DISTINCT(COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' ORDER BY ORDINAL_POSITION"
                results = self.send_query(query)
                
                if table == "reference_list":
                    table = "references"

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
            self.assertEqual(response_list[1], db_columns[1])
            
            ## Check if the last row is the same
            self.assertEqual(response_list[-1], db_columns[-1])

    def test_return_ref_w_good_id(self):
        #Arrange
        ref_id = 174
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
            if table == "references":
                table = "reference_list"

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

    def test_return_international_hourly_transfers(self):
        ##Arrange
        province = 'AB'
        us_region = 'US-Montana'
        year = 2018
        query = f"SELECT * FROM international_transfers \
                WHERE province = '{province}' AND \
                us_state = '{us_region}' AND \
                (local_time LIKE '{year}%' OR \
                (local_time LIKE '{int(year) + 1}%' AND \
                annual_hour_ending = 8760));"

        #Act
        db_result = self.send_query(query)
        response = requests.get(BASE + f"international_transfers?year={year}&province={province}&us_region={us_region}")
        response_code = response.status_code
        response_list = response.json()
        response_row = response_list[0].values()

        #Assert
        self.assertEqual(response_code, 200)
        self.assertEqual(type(response_list),list)
        self.assertEqual(len(response_list), len(db_result))
        
        for i,column in enumerate(response_row):
            if type(db_result[0][i]) == datetime.datetime:
                db_result[0] = list(db_result[0])
                db_result[0][i] = str(db_result[0][i])
            if type(db_result[0][i]) == decimal.Decimal:
                    db_result[0] = list(db_result[0])
                    db_result[0][i] = float(db_result[0][i])
            self.assertEqual(column,db_result[0][i])

    def test_return_interprovincial_hourly_transfers(self):
        ##Arrange
        province_1 = 'BC'
        province_2 = 'AB-AESO'
        year = 2018
        query = f"SELECT * FROM interprovincial_transfers \
                WHERE province_1 = '{province_1}' AND \
                province_2 = '{province_2}' AND \
                (local_time LIKE '{year}%' OR \
                (local_time LIKE '{int(year) + 1}%' AND \
                annual_hour_ending = 8760));"

        #Act
        db_result = self.send_query(query)
        response = requests.get(BASE + f"interprovincial_transfers?year={year}&province1={province_1}&province2={province_2}")
        response_code = response.status_code
        response_list = response.json()
        response_row = response_list[0].values()
        
        #Assert
        self.assertEqual(response_code, 200)
        self.assertEqual(type(response_list),list)
        self.assertEqual(len(response_list), len(db_result))
        for i,column in enumerate(response_row):
            if type(db_result[0][i]) == datetime.datetime:
                db_result[0] = list(db_result[0])
                db_result[0][i] = str(db_result[0][i])
            if type(db_result[0][i]) == decimal.Decimal:
                    db_result[0] = list(db_result[0])
                    db_result[0][i] = float(db_result[0][i])
            self.assertEqual(column,db_result[0][i])

    def test_return_provincial_hourly_demand(self):
        ##Arrange
        province = 'AB'
        year = 2018
        query = f"SELECT * FROM provincial_demand \
                WHERE province = '{province}' AND \
                (local_time LIKE '{year}%' OR \
                (local_time LIKE '{int(year) + 1}%' AND \
                annual_hour_ending = 8760));"

        #Act
        db_result = self.send_query(query)
        response = requests.get(BASE + f"provincial_demand?year={year}&province={province}")
        response_code = response.status_code
        response_list = response.json()
        response_row = response_list[0].values()

        #Assert
        self.assertEqual(response_code, 200)
        self.assertEqual(type(response_list),list)
        self.assertEqual(len(response_list), len(db_result))
        for i,column in enumerate(response_row):
            if type(db_result[0][i]) == datetime.datetime:
                db_result[0] = list(db_result[0])
                db_result[0][i] = str(db_result[0][i])
            if type(db_result[0][i]) == decimal.Decimal:
                    db_result[0] = list(db_result[0])
                    db_result[0][i] = float(db_result[0][i])
            self.assertEqual(column,db_result[0][i])

    def test_return_generator_type(self):
        #Arrange
        province = 'AB'
        gen_type = 'biomass'
        query = f"SELECT * FROM generators WHERE province = 'AB' AND gen_type_copper = 'biomass';"

        #Act
        db_result = self.send_query(query)
        response = requests.get(BASE + f"generators?province={province}&type=biomass")
        response_code = response.status_code
        response_list = response.json()
        response_row = response_list[0].values()

        #Asser
        self.assertEqual(response_code, 200)
        self.assertEqual(type(response_list),list)
        self.assertEqual(len(response_list), len(db_result))
        for i,column in enumerate(response_row):
            if type(db_result[0][i]) == decimal.Decimal:
                    db_result[0] = list(db_result[0])
                    db_result[0][i] = float(db_result[0][i])
            self.assertEqual(column,db_result[0][i])

if __name__ == '__main__':
	unittest.main()