import requests

BASE = "http://127.0.0.1:5000/"

print("####Reference Test#####")
response = requests.get(BASE + "/tables/reference-list/1")
print(response.json())

print("\n####Print Tables Test#####")
response = requests.get(BASE + "/tables")
print(response.json())

print("\n####Print Columns From Table#####")
response = requests.get(BASE + "/tables/nodes/attributes")
print(response.json())

print("\n####Print Rows From Specific Table (this example only prints one row)#####")
response = requests.get(BASE + "/tables/nodes")
for row in response.json():
    print(row)
    break

print("\n####Specify the Province####")
response = requests.get(BASE + "/tables/nodes/NL")
for row in response.json():
    print(row)
    break
#for row in response.json():
 #   print(row)
  #  break