import requests

BASE = "http://127.0.0.1:5000/"

# response = requests.get(BASE)
# print(response.json())

# print("####Reference Test#####")
# response = requests.get(BASE + "reference_list?key=1")
# print(response.json())

# print("\n####Print Tables Test#####")
# response = requests.get(BASE + "/tables")
# print(response.json())

# print("\n####Print Columns From Table#####")
# response = requests.get(BASE + "junctions/attributes")
# print(response.json())

# print("\n####Print Rows From Specific Table (this example only prints one row)#####")
# response = requests.get(BASE + "junctions")
# for row in response.json():
#     print(row)
#     break

# print("\n####Specify the Province####")
# response = requests.get(BASE + "generators?province=NL")
# for row in response.json():
#     print(row)
#     break

# print("\n####International Transfers Test####")
# response = requests.get(BASE + "international_transfers?year=2018&province=AB&us_region=US-Montana")
# for row in response.json():
#     print(row)
#     break
  

# print("\n####Interprovincial Transfers Test####")
# response = requests.get(BASE + "interprovincial_transfers?year=2018&province1=AB&province2=SK")
# for row in response.json():
#     print(row)
#     break

# print("\n####Provincial Demand Test####")
# response = requests.get(BASE + "provincial_demand?year=2018&province=AB")
# for row in response.json():
#     print(row)
#     break

#####Failure Test#####
# response = requests.get(BASE + "/tables/not_real")
# print(response.json())

# response = requests.get(BASE + "/tables/not_real/attributes")
# print(response.json())

# response = requests.get(BASE + "/tables/not_real/BC")
# print(response.json())

# response = requests.get(BASE + "/tables/provincial_demand/2011_AB")
# print(response.json())

# response = requests.post(BASE)
# print(response.json())

# response = requests.get(BASE + "/generators?province=NL&type=hydro_daily")
# #print(response.json())
# for row in response.json():
#     print(row)
#     break

# response = requests.get(BASE + "/filters")
# print(response.json())