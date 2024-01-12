import csv
import json
import requests

def csv_to_json(csvFilePath):
    jsonArray = []
      
    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)
  
    #convert python jsonArray to JSON String and write to file
    # with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
    #     jsonString = json.dumps(jsonArray, indent=4)
    #     jsonf.write(jsonString)
        return jsonArray

def send_request(url:str,data:list,key:str):
    print(data)
    headers = {"Content-Type": "application/json"}

    for data_point in data:
        jBody = {}
        jBody[key] = data_point
        response = requests.request("POST", url, json=jBody, headers=headers)
        print(response.text)


def main():
    url = 'http://127.0.0.1:5000/'
    endpoint = input("please insert url endpoint\n")
    test_file = input("please insert test file\n")
    key = input("Please insert identifier\n")
    url += endpoint
    dict_list = csv_to_json(test_file)
    # changing strings to integer on python
    send_request(url,dict_list,key)

    return

if(__name__=='__main__'):
    main()