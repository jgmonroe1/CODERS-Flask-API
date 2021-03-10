from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import sys
import yaml
import os

app = Flask(__name__)

##Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

def send_query(query):
    cur = mysql.connection.cursor()
    try:
        cur.execute(query)
        result = cur.fetchall()
        return result
    except:
        return 0

def get_columns(table):
    columns = []
    query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' ORDER BY ORDINAL_POSITION"
    results = send_query(query)
    for column in results:
        columns.append(column[0])
    return columns


##Returns a list of the tables in the DB
@app.route('/tables', methods=['GET'])
def show_db_tables():
    query = "SHOW tables;"
    results = send_query(query)
    tables = jsonify(results)
    return tables

##Returns the full table 
@app.route('/tables/<string:table>', methods=['GET'])
def return_table(table):
    ##get the columns from the specified table
    column_names = get_columns(table)
    if column_names == 0:
        return "Table does not exist."
    
    ##send the query
    query = f"SELECT * FROM {table};"
    result = send_query(query)

    ##the table name is incorrect
    if result == 0:
        return  jsonify("Table does not exist")
    result = list(result)
    ##formats the list to "'column_name': 'value'"
    for row_idx,row in enumerate(result):
        row = list(row)
        for i,column in enumerate(row):
            row[i] = {column_names[i]: column}    
        result[row_idx] = row
    return jsonify(result)

##Returns the columns from a specified table
@app.route('/tables/<string:table>/attributes', methods=['GET'])
def return_columns(table):
    query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' ORDER BY ORDINAL_POSITION"
    attributes = send_query(query)

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
    ##query the table based on province
    query = f"SELECT * FROM {table} WHERE province = '{province}';"
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
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))