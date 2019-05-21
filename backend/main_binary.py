from flask import Flask, jsonify, render_template, request
from elasticsearch import Elasticsearch
import skfuzzy as fuzz
import numpy as np
from collections import Counter
import json

from backend.binaryFunctions import binary_search


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
app = Flask(__name__) #Create the flask instance, __name__ is the name of the current Python module
# priceDict = {}
# hdDict = {}
# productTitleDict = {}
# allDocs ={}

# @app.route('/search')
# def index():
#     return render_template('main.html')


@app.route('/api/search', methods=['POST'])
def search():

  data = request.get_json()
  print(data)
  minPrice = request.form['minPrice']
  maxPrice = request.form['maxPrice']
  #hardDrive = request.form['hardDrive']
  hardDriveSize = data['hardDriveSize']

  resBinary = binary_search.BinarySearch.computeBinary(es, minPrice, maxPrice, hardDriveSize)if minPrice and maxPrice and hardDriveSize else {}
  resList = [dict(x) for x in (resBinary, )]


  #Counter objects count the occurrences of objects in the list...
  #count_dict contains each object from resList, and sums the scores for all occurrences. So if asin B07.. occurs
  # twice with a score of 1.0, then it has a score of 2.0 in count_dict
  count_dict = Counter()
  for tmp in resList:
      count_dict += Counter(tmp)

  ####new from beshoy
  # convert counter to dictionary
  result = dict(count_dict)
  print("result")
  print(result)

  # get the keys(asin values)
  asinKeys = list(result.keys())
  print("asinKeys")
  print(asinKeys)

  # call the search function
  outputProducts = getElementsByAsin(asinKeys)

  # add a vagueness score to the returned objects
  for item in outputProducts:
    item['vaguenessScore'] = result[item['asin']]

  #####end beshoy's part
  # to make sure that the items sorted based on the vagueness score just uncomment the next block
  # outputProducts = []
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

  # sort abon the vagueness score
  print("output is: ")
  print(outputProducts)
  outputProducts = sorted(outputProducts, key=lambda x: x["vaguenessScore"], reverse=True)

  #
  # # print("count_dict")
  # # print(count_dict)
  # # print("dict(count_dict).items()")
  # # print(dict(count_dict).items()) #contains pairs
  #
  # #count_dict is a dictionary of key/value pairs. Below is a list comprehension (for dictionaries?) to get key k and value v from each pair (k,v)
  # outputProducts = [("ASIN: {}".format(k), "Product Title: {}".format(productTitleDict[k]), "Vagueness Score: {}".format(v/2),
  #                    "Price: {}".format(priceDict[k]), "Hard Drive Size: {}".format(hdDict[k])) for k, v in dict(count_dict).items()]
  #
  # outputProducts = sorted(outputProducts, key=lambda x: x[2], reverse=True)

  return jsonify(outputProducts) #original from alfred


@app.route('/api/sample', methods=['GET'])
def getSample():
  allDocs = es.search(index="amazon", body={
    "query": {
      "match": {
        "avgRating": 5
      }
    },
    "size": 10
  })

  outputProducts = refineResult(allDocs)
  return jsonify(outputProducts)  # original from alfred


def refineResult(docs):
  outputProducts = []

  for hit in docs['hits']['hits']:
    item = {
      "asin": hit['_source']['asin'],
      "productTitle": hit['_source']['productTitle'],
      "price": hit['_source']['price'],
      "screenSize": hit['_source']['screenSize'],
      "displayResolutionSize": [hit['_source']['displayResolutionSize'][0], hit['_source']['displayResolutionSize'][1]],
      "processorSpeed": hit['_source']['processorSpeed'],
      "processorType": hit['_source']['processorType'],
      "processorCount": hit['_source']['processorCount'],
      "processorManufacturer": hit['_source']['processorManufacturer'],
      "ram": hit['_source']['ram'],
      "brandName": hit['_source']['brandName'],
      "hardDriveType": hit['_source']['hardDriveType'],
      "ssdSize": hit['_source']['ssdSize'],
      "hddSize": hit['_source']['hddSize'],
      "graphicsCoprocessor": hit['_source']['graphicsCoprocessor'],
      "chipsetBrand": hit['_source']['chipsetBrand'],
      "operatingSystem": hit['_source']['operatingSystem'],
      "itemWeight": hit['_source']['itemWeight'],
      # "memoryType": hit['_source']['memoryType'],
      "productDimension": [hit['_source']['productDimension'][0], hit['_source']['productDimension'][0],
                           hit['_source']['productDimension'][0]],
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
  print("What is asinKeys")
  print(asinKeys)

  result = es.search(index="amazon", body={
    "query": {
      "terms": {
        "asin.keyword": asinKeys
      }
    }
  })
  print("elastic search result")
  print(result)
  return refineResult(result)


if __name__ == "__main__":
    app.run(debug=True)
