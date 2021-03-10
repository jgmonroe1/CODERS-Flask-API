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

# @app.route('/', methods=['GET','POST'])
# def index():
#     if request.method == "POST":
#         ##fetch form data
#         userDetails = request.form
#         sub_name = f"\'{userDetails['sub_name']}\'"
#         sub_code = f"\'{userDetails['sub_code']}\'"
#         cur = mysql.connection.cursor()
#         cur.execute(f"INSERT INTO nodes (name, node_code) VALUES({sub_name},{sub_code});")
#         cur.execute(f"INSERT INTO substations (sub_node_code) VALUES({sub_code});")
#         mysql.connection.commit()
#         cur.close()
    
#         return "success"
#     return render_template('index.html')
def get_columns(table):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' ORDER BY ORDINAL_POSITION")
        columns = []
        for column in cur.fetchall():
            columns.append(column[0])
        return columns
    except mysql.connector.Error as err:
        return 0

@app.route('/tables', methods=['GET'])
def show_db_tables():
    cur = mysql.connection.cursor()
    cur.execute("SHOW tables;")
    cur.close()
    result = jsonify(cur.fetchall())
    return result

@app.route('/tables/<string:table>', methods=['GET'])
def return_table(table):
    column_names = get_columns(table)
    if column_names == 0:
        return "Table does not exist."
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM {table};")
    result = list(cur.fetchall())
    for row_idx,row in enumerate(result):
        row = list(row)
        for i,column in enumerate(row):
            row[i] = {column_names[i]: column}    
        result[row_idx] = row
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))