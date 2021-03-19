from flask import Flask, render_template, request, jsonify, Response
from flask_mysqldb import MySQL
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sys
import yaml
import os
import json

from classes.invalidUsage import InvalidUsage
from classes.encoder import Encoder

app = Flask(__name__)

##Configure db
db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host'] #host.docker.internal
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

#Rate Limiter
#====================================================================
Limiter = Limiter(app,key_func=get_remote_address)

#Error Handling
#====================================================================
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

#Defining Variables
#====================================================================
##the list of tables the user can request
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

gen_types = ("wind",
            "gas",
            "waste",
            "coal",
            "solar",
            "hydro_run",
            "hydro_daily",
            "hydro_monthly",
            "peaker",
            "diesel",
            "nuclear",
            "hydro_pump")

#Helper Methods
#====================================================================
##Executes the query to the database
def send_query(query):
    cur = mysql.connection.cursor()
    try:
        cur.execute(query)
        result = cur.fetchall()
        return list(result)
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
        if results == 0:
            return 0
        for column in results:
            columns.append(column[0])
    return columns



#API Routes
#====================================================================
##Initial connection message
@app.route('/', methods=['GET'])
@Limiter.limit('100 per second')
def start_up():
    welcome_msg = "Welcome to the CODERS database!\n"
    functions = "For the list of tables:\n\
                    http://[domain]/tables\n\n\
                For a full query of a specified table:\n\
                    http://[domain]/[table]\n\n\
                For a list of columns in a specified table:\n\
                    http://[domain]/[table]/attributes\n\n\
                For the results of a query filtered by province:\n\
                    http://[domain]/[table]?province=[province]\n\n\
                For the hourly transfers between a specified province and US state over a specified year:\n\
                    http://[domain]/international_transfers?year=[year]&province=[province]&us_region=[state]\n\n\
                For the hourly transfers between two provinces over a specified year:\n\
                    http://[domain]/interprovincial_transfers?year=[year]&province1=[province]&province2=[province]\n\n\
                For the hourly demand in a specified province:\n\
                    http://[domain]/provincial_demand?year=[year]&province=[province]\n\n\
                For the generators filtered by province and generation type:\n\
                    http://[domain]/generators?province=[province]&type=[generation_type]\n\n\
                For locating a reference:\n\
                    http://[domain]/references?key=[reference_key]\n".replace('  ','')
    return jsonify(welcome_msg + functions)

##Returns the available filters
@app.route('/filters', methods=['GET'])
def return_filters():
    filters = "Province: substations, generators, transmission_lines, junctions, interties, storage_batteries\n\
                Province and Generation Type: generators\n\
                Reference Key: references\n\
                Year, Province, and US Region: international_transfers\n\
                Year, Province, and Province: interprovincial_transfers\n\
                Year and Province: provincial_demand\n".replace('  ', '')
    return jsonify(filters)

##Returns a list of the tables in the DB
@app.route('/tables', methods=['GET'])
@Limiter.limit('100 per second')
def show_db_tables():
    return json.dumps(accessible_tables, cls= Encoder)

##Returns the full table 
@app.route('/<string:table>', methods=['GET'])
@Limiter.limit('100 per second')
def return_table(table):
    ## Check if the table exists
    if table not in accessible_tables:
        raise InvalidUsage('Table not recognized',status_code=404)

    ## Parse the request for different parameters
    province = request.args.get('province')
    reference_key = request.args.get('key')
    gen_type = request.args.get('type')
    year = request.args.get('year')
    us_region = request.args.get('us_region')
    province_1 = request.args.get('province1')
    province_2 = request.args.get('province2')
    ## Redirect to the generator type filter
    if table == 'generators' and province and gen_type:
        return return_generator_type(province, gen_type)
    ## Redirect to the reference list
    elif table == 'references' and reference_key:
        return return_ref(reference_key)
    ## Redirect to international transfers
    elif table == 'international_transfers' and year and province and us_region:
        return return_international_hourly_transfers(year, province, us_region)
    ## Redirect to interprovincial transfers
    elif table == 'interprovincial_transfers' and year and province_1 and province_2:
        return return_interprovincial_hourly_transfer(year, province_1, province_2)
    ## Redirect to provincal demand
    elif table == 'provincial_demand' and year and province and not us_region:
        return return_provincial_hourly_demand(year, province)
    ## Redirect to the province filter
    elif province:
        return return_based_on_prov(table, province)
    
    ## Join the subtables on the node table
    if table == "junctions":
        table = "nodes"
        query = f"SELECT * FROM {table} WHERE node_type = 'JCT';"
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
    ## Table is not substations, junctions, or interties
    else:
        query = f"SELECT * FROM {table};"

    ## Get the column names and send the query
    column_names = get_columns(table)
    result = send_query(query)

    ## Format the list to "'column_name': 'value'"
    for row_idx,row in enumerate(result):
        row = list(row)
        for i,column in enumerate(row):
            row[i] = {column_names[i]: column}    
        result[row_idx] = row

    return json.dumps(result, cls= Encoder)

##Returns the columns from a specified table
@app.route('/<string:table>/attributes', methods=['GET'])
@Limiter.limit('100 per second')
def return_columns(table):
    ## Check if the table exists
    if table not in accessible_tables:
        raise InvalidUsage('Table not recognized',status_code=404)
    
    if table == "junctions":
        table = "nodes"
    
    ## Get the column names
    attributes = get_columns(table)

    return json.dumps(attributes, cls= Encoder)

##Returns the reference from the given reference key
def return_ref(key):
    if not isinstance(key, int) or int(key) <= 0:
        raise InvalidUsage('Key must be a positive integer', status_code=404)

    ## Query the reference list
    query = f"SELECT * FROM reference_list WHERE id = {key}"
    source = send_query(query)

    #Check if the source was found
    if source == 0:
        raise InvalidUsage('Key was invalid', status_code=404)
    elif len(source) == 0:
        raise InvalidUsage('Key was not associated with any reference', status_code=404)
    
    ## Get the column names from the reference list
    column_names = get_columns("reference_list")
    
    ## Format the list to "column_name: value"
    for row_idx,row in enumerate(source):
        row = list(row)
        for i,column in enumerate(row):
            row[i] = {column_names[i]: column}    
        source[row_idx] = row
    
    return json.dumps(source, cls= Encoder)

##Returns the specified table based on Province
def return_based_on_prov(table, province):
    if table not in accessible_tables:
        raise InvalidUsage('Table not recognized',status_code=404)
    
    ## Query interties joined on nodes
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
    ## Query only the junction types from the node table
    elif table == "junctions":
        table = "nodes"
        query = f"SELECT * FROM {table} WHERE province = '{province}' \
                AND node_type = 'JCT';"
    ## Query for the rest of the tables
    elif table in ("generators","transmission_lines","storage_batteries"):
        query = f"SELECT * FROM  {table} WHERE province = '{province}'"
    else:
        raise InvalidUsage('Table has no province attribute',status_code=400)

    result = send_query(query)

    ## Get the column names
    column_names = get_columns(table)

    ## Handling bad requests and empty tables
    if result == 0:
        raise InvalidUsage('Invalid province',status_code=400)
    elif len(result) == 0:
        raise InvalidUsage('No results found',status_code=404)
    
    ## Format the list to "'column_name': 'value'"
    for row_idx,row in enumerate(result):
        row = list(row)
        for i,column in enumerate(row):
            row[i] = {column_names[i]: column}    
        result[row_idx] = row

    return json.dumps(result, cls= Encoder)

##Returns the transfers between a specified province and US region
def return_international_hourly_transfers(year, province, state):
    query = f"SELECT * FROM international_transfers \
                WHERE province = '{province}' AND \
                us_state = '{state}' AND \
                local_time LIKE '{year}%'"

    result = send_query(query)
    ## Handling empty tables and bad requests
    if result == 0:
        raise InvalidUsage('Invalid province, state, year combination',status_code=400)
    elif len(result) == 0:
        raise InvalidUsage('No results found',status_code=404)

    column_names = get_columns("international_transfers")

    ## Format the list to "'column_name': 'value'"
    for row_idx,row in enumerate(result):
        row = list(row)
        for i,column in enumerate(row):
            row[i] = {column_names[i]: column}    
        result[row_idx] = row
    return json.dumps(result, cls= Encoder)

##Returns the transfers between two specified provinces
def return_interprovincial_hourly_transfer(year, province_1, province_2):
    query = f"SELECT * FROM interprovincial_transfers \
                WHERE province_1 = '{province_1}' AND \
                province_2 = '{province_2}' AND \
                local_time LIKE '{year}%';"
    result = send_query(query)

    ## Handling empty tables and bad requests
    if result == 0:
        raise InvalidUsage('Invalid province, province, year combination',status_code=400)
    elif len(result) == 0:
        raise InvalidUsage('No results found',status_code=404)
    column_names = get_columns("interprovincial_transfers")

    ## Format the list to "'column_name': 'value'"
    for row_idx,row in enumerate(result):
        row = list(row)
        for i,column in enumerate(row):
            row[i] = {column_names[i]: column}    
        result[row_idx] = row
    return json.dumps(result, cls= Encoder)

##Returns the demand in a specified province
def return_provincial_hourly_demand(year, province):
    query = f"SELECT * FROM provincial_demand \
                WHERE province = '{province}' AND \
                local_time LIKE '{year}%'"
    
    result = send_query(query)
    ## Handling bad requests
    if result == 0:
        raise InvalidUsage('Invalid province and year combination',status_code=400)
    elif len(result) == 0:
        raise InvalidUsage('No results found',status_code=404)
    column_names = get_columns("provincial_demand")

    ## Format the list to "'column_name': 'value'"
    for row_idx,row in enumerate(result):
        row = list(row)
        for i,column in enumerate(row):
            row[i] = {column_names[i]: column}    
        result[row_idx] = row
    return json.dumps(result, cls= Encoder)

##Returns generators filtered by generation type
def return_generator_type(province, gen_type):
    ## Handling unknown generator type
    if gen_type not in gen_types:
        raise InvalidUsage('Invalid generator type',status_code=404)
    query = f"SELECT * FROM generators \
                WHERE gen_type_copper = '{gen_type}' AND \
                province = '{province}';"
    
    result = send_query(query)

    ## Handling bad requests and empty tables
    if len(result) == 0:
        raise InvalidUsage(f"No {gen_type} generators found in {province}", status_code=404)
    elif result == 0:
        raise InvalidUsage('Invalid generator type or province', status_code=400)

    column_names = get_columns("generators")

    ## Formats the list to "'column_name': 'value'"
    for row_idx,row in enumerate(result):
        row = list(row)
        for i,column in enumerate(row):
            row[i] = {column_names[i]: column}    
        result[row_idx] = row
    return json.dumps(result, cls= Encoder)


if __name__ == '__main__':
    #app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    app.run(debug=True)