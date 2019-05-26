import collections

from flask import Flask, jsonify, render_template, request
from elasticsearch import Elasticsearch
import skfuzzy as fuzz
import numpy as np
from collections import Counter
#from flask_cors import CORS
import json


from vagueFunctions import vague_search_price, vague_search_harddrive,vague_search_range
from binaryFunctions import binary_search_text

#from backend.vagueFunctions import vague_search_price, vague_search_harddrive
#from backend.binaryFunctions import binary_search_text

# from vagueFunctions import vague_search_price, vague_search_harddrive,vague_search_hdType



es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
app = Flask(__name__) #Create the flask instance, __name__ is the name of the current Python module

# priceDict = {}
# productTitleDict = {}
# hdTypeDict = {}
# hddSizeDict = {}
# ssdSizeDict= {}


# @app.route('/')
# def index():
#     return render_template('main.html')\

def callAttributeMethod(attributeName,attributeValue,attributeWeight,allDocs) :
    methodName = "computeVague"+attributeName[0].upper()+attributeName[1:]
    className = "vague_search_"+attributeName

    eval(className+"."+methodName)

def extract_fields_and_values(fieldNameToValueDict) :

    result = dict(dict())

    for fieldName in fieldNameToValueDict :

        if not fieldNameToValueDict[fieldName]:
            continue
        #normal match
        #Ranged terms, example : ram : { minRam : 2,maxRam : 4}
        #If that's the case, then search for minRam and maxRam in fieldNameToValueDict, get them and add range to the query
        if type(fieldNameToValueDict[fieldName]) is dict and ("minValue" in fieldNameToValueDict[fieldName] or "maxValue" in fieldNameToValueDict[fieldName]) :
            #Extract name of field, and set the name of min and max values to minField and maxField, example : minRam and maxRam.
            #minValueName = "min"+fieldName[0].upper()+fieldName[1:]
            #maxValueName = "max"+fieldName[0].upper()+fieldName[1:]


            #Extract the values of minField and maxField from the JSON coming from the front end
            if "minValue" in fieldNameToValueDict[fieldName] and  "maxValue" in fieldNameToValueDict[fieldName] :
                result["range"].append(fieldName :{"minValue" :fieldNameToValueDict[fieldName]["minValue"]
                ,"maxValue" : fieldNameToValueDict[fieldName]["minValue"]
                ,"weight" :fieldNameToValueDict[fieldName]["weight"] } )

            elif "minValue" in fieldNameToValueDict[fieldName] :
                result["range"].append(fieldName :{"minValue" :fieldNameToValueDict[fieldName]["minValue"] ,"weight" :fieldNameToValueDict[fieldName]["weight"]} )

            elif"maxValue" in fieldNameToValueDict[fieldName] :
                result["range"].append(fieldName :{"maxValue" :fieldNameToValueDict[fieldName]["maxValue"],"weight" :fieldNameToValueDict[fieldName]["weight"] } )

        #--------------------------------------------------------------------------------------------------------------------------------#
        #In case of multiple values for the same field, example : ram : [2,4,6], ram is either 2, 4 or 6.
        elif "value" in fieldNameToValueDict[fieldName] :
            if type(fieldNameToValueDict[fieldName]["value"]) is list :
                if type(fieldNameToValueDict[fieldName][0]) is str :
                    fieldNameToValueDict[fieldName] = [x.lower() for x in fieldNameToValueDict[fieldName]]
        #--------------------------------------------------------------------------------------------------------------------------------#
        #A normal numerical match, example : ram : 8, ram is 8
            elif type(fieldNameToValueDict[fieldName]["value"]) is int or type(fieldNameToValueDict[fieldName]["value"]) is float :
                result["vague"].append(fieldName :{"value" :fieldNameToValueDict[fieldName]["value"],"weight" :fieldNameToValueDict[fieldName]["weight"] } )
            #--------------------------------------------------------------------------------------------------------------------------------#
            #A normal string match as brandName or hardDriveType
            else :
                #Example : match "{ ram : 8}"
                result["binary"].append(fieldName :{"value" :fieldNameToValueDict[fieldName]["value"],"weight" :fieldNameToValueDict[fieldName]["weight"] } )
            #--------------------------------------------------------------------------------------------------------------------------------#

    return result


    return body


@app.route('/api/search', methods=['POST'])
def search():

    data = request.get_json()
    minPrice = None
    maxPrice = None
    hardDriveType = None
    if 'price' in data:
        if 'minValue' in data['price'] and data['price']['minValue']:
            minPrice = data['price']['minValue']

        if 'maxValue' in data['price'] and data['price']['maxValue']:
            maxPrice = data['price']['maxValue']

    if 'hardDriveSize' in data:
       hardDriveSize = data['hardDriveSize']
    else:
      hardDriveSize = None

     #Extracts each field and its value and weight to the dict
     field_value_dict =  extract_fields_and_values(data)

     for field_type in field_value_dict.keys() :
         for field_name in field_value_dict[field_type].keys() :
             field_name = field_value_dict[field_type][field_name]
             field_weight = field_value_dict[field_type]["weight"]
             if field_type is "binary" :
                 field_value = field_value_dict[field_type][field_name]["value"]
                 compute_vague_value(field_name,field_weight,field_value)
                 pass
             elif field_type is "range" :
                 if "minValue" in field_value_dict[field_type][field_name].keys() and  "maxValue" in field_value_dict[field_type][field_name].keys() :
                     min_value =field_value_dict[field_type][field_name]["minValue"]
                     max_value =field_value_dict[field_type][field_name]["maxValue"]
                     compute_vague_range(field_name,field_weight,min_value,max_value)
                elif "minValue" in field_value_dict[field_type][field_name].keys() :
                     min_value =field_value_dict[field_type][field_name]["minValue"]
                     compute_vague_range(field_name,field_weight,min_value,None)

                elif "maxValue" in field_value_dict[field_type][field_name].keys() :
                     max_value =field_value_dict[field_type][field_name]["maxValue"]
                     compute_vague_range(field_name,field_weight,None,max_value)

             elif field_type is "vague" :
                 field_value = field_value_dict[field_type][field_name]["value"]
                 compute_vague_value(field_name,field_weight,field_value)
                 pass


  #CLEANUP later...
   # print(data)
   # minPrice = data['minPrice']
   # maxPrice = data['maxPrice']
    # hardDriveType = data['hardDriveType']
   # hardDriveSize = data['hardDriveSize']


    if 'hardDriveType' in data:
      hardDriveType = data['hardDriveType']


    allDocs = es.search(index="amazon", body={
                                                "size": 10000,
                                                "query": {
                                                    "match_all": {}
                                                    }
                                                })

    pr = vague_search_price.VagueSearchPrice(es)
    resVagueListPrice = pr.computeVaguePrice(allDocs, minPrice, maxPrice) if minPrice and maxPrice else {}

    hd = vague_search_harddrive.VagueHardDrive(es)
    resVagueListHardDrive = hd.computeVagueHardDrive(allDocs, hardDriveSize) if hardDriveSize else {}

    data1 = {'brandName': brandName}
    br = binary_search_text.BinarySearchText(es)

    binaryListBrand = br.compute_binary_text(data1) if brandName else {}

    data1= {'hardDriveType': hardDriveType}
    binaryListHardDriveType = br.compute_binary_text(data1) if hardDriveType else {}


    #resList is a list containing a dictionary of ASIN: score values
    #resList = [dict(x) for x in (resVagueListPrice, resVagueListHardDrive)]
    resList = [dict(x) for x in (resVagueListPrice,
                                 resVagueListHardDrive,
                                 # binaryListBrand,
                                 binaryListHardDriveType)
               ]


    # print("printing resList")
    # print(resList)

    #Counter objects count the occurrences of objects in the list...
    count_dict = Counter()
    for tmp in resList:
        count_dict += Counter(tmp)

    ####new from beshoy
    #convert counter to dictionary
    result = dict(count_dict)
    # print("result")
    # print(result)


    sortedDict = collections.OrderedDict(sorted(result.items(), key=lambda x: x[1], reverse=True))
    print("sort result dict")
    print(sortedDict)

    #get the keys(asin values)
    asinKeys = list(result.keys())
    # print("asinKeys")
    # print(asinKeys)

    #call the search function
    outputProducts = getElementsByAsin(asinKeys)


    #add a vagueness score to the returned objects
    for item in outputProducts:
      item['vaguenessScore'] = result[item['asin']]


    #####end beshoy's part
    #to make sure that the items sorted based on the vagueness score just uncomment the next block
    #outputProducts = []
    # for (k, v) in result.items():
    #     item = {
    #         "ASIN": k,
    #         "ProductTitle": productTitleDict[k],
    #         "Vagueness Score": v/2,
    #         "price": priceDict[k],
    #         "Hard Drive Size": hdSizeDict[k],
    #         "Hard Drive type": hdTypeDict[k]
    #     }
    #     outputProducts.append(item)

    #sort abon the vagueness score

    print("unsorted output is: ")
    print(outputProducts)
    outputProducts =sorted(outputProducts, key=lambda x: x["vaguenessScore"], reverse=True)
    print("sorted output is: ")
    print(outputProducts)



    return jsonify(outputProducts)


@app.route('/api/sample', methods=['GET'])
def getSample():
    allDocs = es.search(index="amazon", body ={
                                                "query": {
                                                    "match": {
                                                        "avgRating": 5
                                                        }
                                                    },
                                                "size" : 10
                                              })

    outputProducts = refineResult(allDocs)
    return jsonify(outputProducts) #original from alfred


def refineResult(docs):
    outputProducts = []

    for hit in docs['hits']['hits']:
        item = {
          "asin": hit['_source']['asin'],
          "productTitle": hit['_source']['productTitle'],
          "price": hit['_source']['price'],
          "screenSize" : hit['_source']['screenSize'],
          "displayResolutionSize" : [hit['_source']['displayResolutionSize'][0], hit['_source']['displayResolutionSize'][1]],
          "processorSpeed" : hit['_source']['processorSpeed'],
          "processorType" : hit['_source']['processorType'],
          "processorCount" : hit['_source']['processorCount'],
          "processorManufacturer" : hit['_source']['processorManufacturer'],
          "ram" : hit['_source']['ram'],
          "brandName" : hit['_source']['brandName'],
          "hardDriveType" : hit['_source']['hardDriveType'],
          "ssdSize" : hit['_source']['ssdSize'],
          "hddSize": hit['_source']['hddSize'],
          "graphicsCoprocessor": hit['_source']['graphicsCoprocessor'],
          "chipsetBrand": hit['_source']['chipsetBrand'],
          "operatingSystem": hit['_source']['operatingSystem'],
          "itemWeight": hit['_source']['itemWeight'],
          #"memoryType": hit['_source']['memoryType'],
          "productDimension": [hit['_source']['productDimension'][0],hit['_source']['productDimension'][0],hit['_source']['productDimension'][0]],
          "color": hit['_source']['color'],
          "imagePath": hit['_source']['imagePath'],
          "avgRating": hit['_source']['avgRating'],

        }
        outputProducts.append(item)
    return outputProducts

# def dicts(docs):
#
#   for hit in docs['hits']['hits']:
#     productTitleDict[hit['_source']['asin']] = hit['_source']['productTitle']
#     priceDict[hit['_source']['asin']] = float(hit['_source']['price'])
#     displaySizeDict[hit['_source']['asin']] = hit['_source']['displaySize']
#     screenResoultionSizeDict[hit['_source']['asin']] = [hit['_source']['screenResoultionSize'][0], hit['_source']['screenResoultionSize'][1]]
#     processorSpeedDict[hit['_source']['asin']] = hit['_source']['processorSpeed']
#     processorTypeDict[hit['_source']['asin']] = hit['_source']['processorType']
#     processorCountDict[hit['_source']['asin']] = hit['_source']['processorCount']
#     processorBrandDict[hit['_source']['asin']] = hit['_source']['processorBrand']
#     ramDict[hit['_source']['asin']] = hit['_source']['ram']
#     brandNameDict[hit['_source']['asin']] = hit['_source']['hardDriveType']
#     hdTypeDict[hit['_source']['asin']] = hit['_source']['hardDriveType']
#     ssdSizeDict[hit['_source']['asin']] = float(hit['_source']['ssdSize']) if hit['_source']['ssdSize'] else 0
#     hddSizeDict[hit['_source']['asin']] = float(hit['_source']['hddSize']) if hit['_source']['hddSize'] else 0
#     graphicsCoprocessorDict[hit['_source']['asin']] = hit['_source']['graphicsCoprocessor']
#     chipsetBrandDict[hit['_source']['asin']] = hit['_source']['chipsetBrand']
#     operatingSystemDict[hit['_source']['asin']] = hit['_source']['operatingSystem']
#     itemWeightDict[hit['_source']['asin']] = hit['_source']['itemWeight']
#     productDimensionDict[hit['_source']['asin']] = [hit['_source']['productDimension'][0],hit['_source']['productDimension'][0],hit['_source']['productDimension'][0]]
#     colorDict[hit['_source']['asin']] = hit['_source']['color']
#     imagePathDict[hit['_source']['asin']] = hit['_source']['imagePath']
#     avgRatingDict[hit['_source']['asin']] = hit['_source']['avgRating']

def getElementsByAsin(asinKeys):
  # print(asinKeys)
  # print(len(asinKeys))
  result = es.search(index="amazon", body={
                                              "query": {
                                                  "terms": {
                                                        "asin.keyword": asinKeys
                                                  }

                                              }, "size":7000

                                            })
  # print("elastic search result")
  # print(result)
  return refineResult(result)


if __name__ == "__main__":
    app.run(debug=True)
