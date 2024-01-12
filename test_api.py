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

def send_request(url:str,data:list):
    print(data)
    headers = {"Content-Type": "application/json"}

    for data_point in data:
        response = requests.request("POST", url, json=data_point, headers=headers)
        print(response.text)


def main():
    path = input("please insert csv file name")
    path = path.strip()
    url = input("please insert url endpoint")
    url.strip()
    dict_list = csv_to_json(path)
    send_request(url,dict_list)

    return