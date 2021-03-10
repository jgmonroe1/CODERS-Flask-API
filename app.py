from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import sys
import yaml
import os

app = Flask(__name__)

##Configure db
db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

##Executes the query to the database
def send_query(query):
    cur = mysql.connection.cursor()
    try:
        cur.execute(query)
        result = cur.fetchall()
        return result
    except:
        return 0

##Returns the columns of a specified table
def get_columns(table):
    columns = []
    if table == 'substations':
        columns = ["name", 
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
        columns = ["name", 
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
    else:   
        query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' ORDER BY ORDINAL_POSITION"
        results = send_query(query)
        for column in results:
            columns.append(column[0])
    return columns

##Returns a list of the tables in the DB
@app.route('/tables', methods=['GET'])
def show_db_tables():
    tables = ["generators",
                "substations",
                "transmission_lines",
                "storage_batteries",
                "interties",
                "distribution_transfers",
                "contribution_transfers",
                "generation_costs",
                "international_transfers",
                "interprovincial_transfers",
                "provincial_transfers",
                "intertie_all",
                "intertie_provincial",
                "cpi_can",
                "reference_list"]

    return jsonify(tables)

##Returns the full table 
@app.route('/tables/<string:table>', methods=['GET'])
def return_table(table):
    ##if the table is sub, jct, or int, join the subtable on the node table
    if table == "junctions":
        table = "nodes"
        query = f"SELECT * FROM {table} WHERE node_type = 'JCT';"
        if column_names == 0:
            return jsonify("Table does not exist.")

    ##Join the substation on the nodes
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
                    JOIN substations s ON n.node_code = s.sub_node_code;"
        
    ##Join the interties on the nodes
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

    ##If not a jct, sub, or int, query the table
    else:
        query = f"SELECT * FROM {table};"
        ##get the columns from the specified table
        column_names = get_columns(table)
        if column_names == 0:
            return jsonify("Table does not exist.")
    
    column_names = get_columns(table)
    
    ##send the query
    result = send_query(query)

    ##the table name is incorrect
    if result == 0:
        return  jsonify("Table is empty.")
    result = list(result)
    ##formats the list to "'column_name': 'value'"
    for row_idx,row in enumerate(result):
        row = list(row)
        for i,column in enumerate(row):
            row[i] = {column_names[i]: column}    
        result[row_idx] = row

    ##Check if the table is empty
    if len(result) == 0:
        return jsonify("Table is empty.")
        
    return jsonify(result)

##Returns the columns from a specified table
@app.route('/tables/<string:table>/attributes', methods=['GET'])
def return_columns(table):
    if table == "junctions":
        table = "nodes"
    
    attributes = get_columns(table)

    ##check if table name is incorrect
    if attributes == 0:
        return jsonify("Table does not exist")

    return jsonify(attributes)
    
##Returns the reference from the given reference key
@app.route('/tables/reference-list/<int:key>', methods=['GET'])
def return_ref(key):
    ##query the ref list
    query = f"SELECT * FROM reference_list WHERE id = {key}"
    source = send_query(query)
    #check if the source was found
    if source == 0:
        return jsonify("Key not found")
    table = "reference_list"

    ##get the column names from the reference list
    column_names = get_columns(table)
    if column_names == 0:
        return "Table does not exist."
    
    ##Format the list to "column_name: value"
    source = list(source)
    for row_idx,row in enumerate(source):
        row = list(row)
        for i,column in enumerate(row):
            row[i] = {column_names[i]: column}    
        source[row_idx] = row
    
    return jsonify(source)

##Returns the specified table based on Province
@app.route('/tables/<string:table>/<string:province>', methods=['GET'])
def return_based_on_prov(table, province):
    ##query for substations joined on nodes
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
    ##query for junctions joined on nodes
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
    ##query only the junction types from the node table
    elif table == "junctions":
        table = "nodes"
        query = f"SELECT * FROM {table} WHERE province = '{province}' \
                AND node_type = 'JCT';"
    
    result = send_query(query)

    ##get the column names
    column_names = get_columns(table)
    if column_names == 0:
        return "Table does not exist."

    ##check if the table and province are valid
    if result == 0:
        return jsonify(f"Province({province}) is invalid")

    result = list(result)
    ##formats the list to "'column_name': 'value'"
    for row_idx,row in enumerate(result):
        row = list(row)
        for i,column in enumerate(row):
            row[i] = {column_names[i]: column}    
        result[row_idx] = row
    
    ##Check if the table is empty
    if len(result) == 0:
        return jsonify("Table is empty.")

    return jsonify(result)

if __name__ == '__main__':
    #app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    app.run(debug=True)