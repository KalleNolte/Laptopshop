import collections

from flask import Flask, jsonify, render_template, request
from elasticsearch import Elasticsearch
import skfuzzy as fuzz
import numpy as np
from collections import Counter
#from flask_cors import CORS
import json
from backend.vagueFunctions import vague_search_price

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
app = Flask(__name__) #Create the flask instance, __name__ is the name of the current Python module

# priceDict = {}
# productTitleDict = {}
# hdTypeDict = {}
# hddSizeDict = {}
# ssdSizeDict= {}


# @app.route('/')
# def index():
#     return render_template('main.html')

@app.route('/api/search', methods=['POST'])
def search():
    data = request.get_json()
    minPrice = data['minPrice']
    maxPrice = data['maxPrice']

    hardDriveType = data['hardDriveType']
    hardDriveSize = data['hardDriveSize']

    # hardDriveType = 'hdd'
    # hardDriveSize = 1000


    allDocs = es.search(index="amazon", body={
                                                "size": 10000,
                                                "query": {
                                                    "match_all": {}
                                                    }
                                                })


    # for hit in allDocs['hits']['hits']:
    #     #print(hit)
    #     priceDict[hit['_source']['asin']] = float(hit['_source']['price'])
    #     hdTypeDict[hit['_source']['asin']] = hit['_source']['hardDriveType']
    #     #ignore hybrid and emmc for now
    #     if hit['_source']['hardDriveType']:
    #         if hit['_source']['hardDriveType'].lower() == 'ssd':
    #             hdSizeDict[hit['_source']['asin']] = float(hit['_source']['ssdSize']) if hit['_source']['ssdSize'] else 0
    #         else:
    #             hdSizeDict[hit['_source']['asin']] = float(hit['_source']['hddSize']) if hit['_source']['hddSize'] else 0
    #     productTitleDict[hit['_source']['asin']] = hit['_source']['productTitle']

    # print("hdSize")
    # print(hdSizeDict)
    #both variables below are lists containing pairs (ASIN, score)

    resVagueListPrice = vague_search_price.VagueSearchPrice.computeVaguePrice(es, allDocs, minPrice, maxPrice) if minPrice and maxPrice else {}

    resVagueListHardDrive = computeVagueHardDrive(es, allDocs, hardDriveSize) if hardDriveSize else {}

    #resList is a list containing a dictionary of ASIN: score values
    resList = [dict(x) for x in (resVagueListPrice, resVagueListHardDrive)]

    # print("printing resList")
    # print(resList)

    #Counter objects count the occurrences of objects in the list...
    count_dict = Counter()
    for tmp in resList:
        count_dict += Counter(tmp)

    # print("count_dict")
    # print(count_dict)

    #convert counter to dictionary
    result = dict(count_dict)
    print("result")
    print(result)

    #get the keys(asin values)
    asinKeys = list(result.keys())
    print("asinKeys")
    print(asinKeys)

    #call the search function
    outputProducts = getElementsByAsin(asinKeys)

    #add a vagueness score to the returned objects
    for item in outputProducts:
      item['vaguenessScore'] = result[item['asin']]


    #count_dict is a dictionary of key/value pairs. Below is a list comprehension (for dictionaries?) to get key k and value v for each item
    # outputProducts = [("ASIN: {}".format(k), "Product Title: {}".format(productTitleDict[k]), "Vagueness Score: {}".format(v/2),
    #                    "Price: {}".format(priceDict[k]), "Hard Drive Size: {}".format(hdDict[k])) for k, v in dict(count_dict).items()]

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
    outputProducts = sorted(outputProducts, key=lambda x: x["vaguenessScore"], reverse=True)


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
          "displaySize" : hit['_source']['displaySize'],
          "screenResoultionSize" : [hit['_source']['screenResoultionSize'][0], hit['_source']['screenResoultionSize'][1]],
          "processorSpeed" : hit['_source']['processorSpeed'],
          "processorType" : hit['_source']['processorType'],
          "processorCount" : hit['_source']['processorCount'],
          "processorBrand" : hit['_source']['processorBrand'],
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
  result = es.search(index="amazon", body={
                                              "query": {
                                                  "terms": {
                                                        "asin.keyword": asinKeys
                                                  }
                                              }
                                            })
  return refineResult(result)


if __name__ == "__main__":
    app.run(debug=True)
