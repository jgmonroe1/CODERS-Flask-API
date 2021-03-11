import requests

BASE = "http://127.0.0.1:5000/"

# response = requests.get(BASE)
# print(response.json())

# print("####Reference Test#####")
# response = requests.get(BASE + "/tables/reference-list/1")
# print(response.json())

# print("\n####Print Tables Test#####")
# response = requests.get(BASE + "/tables")
# print(response.json())

# print("\n####Print Columns From Table#####")
# response = requests.get(BASE + "/tables/cpi_can/attributes")
# print(response.json())

# print("\n####Print Rows From Specific Table (this example only prints one row)#####")
# response = requests.get(BASE + "/tables/substations")
# for row in response.json():
#     print(row)
#     break

# print("\n####Specify the Province####")
# response = requests.get(BASE + "/tables/cpi_can/NL")
# print(response.json())
# for row in response.json():
#     print(row)
#     break

print("\n####International Transfers Test####")
response = requests.get(BASE + "/tables/international_transfers/2018_AB_Montana")
for row in response.json():
    print(row)
    break

print("\n####Interprovincial Transfers Test####")
response = requests.get(BASE + "/tables/interprovincial_transfers/2018_AB_SK")
for row in response.json():
    print(row)
    break

print("\n####Provincial Demand Test####")
response = requests.get(BASE + "/tables/provincial_demand/2018_AB")
for row in response.json():
    print(row)
    break