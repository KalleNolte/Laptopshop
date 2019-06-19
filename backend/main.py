import collections

from flask import Flask, jsonify, render_template, request
from elasticsearch import Elasticsearch
import skfuzzy as fuzz
import numpy as np
from collections import Counter
#from collections
#from flask_cors import CORS
import json
import requests

#
# from vagueFunctions import vague_search_price, vague_search_harddrive,vague_search_range,vague_search_value
# from binaryFunctions import binary_search_text
# from helper import Backend_Helper
# from vagueFunctions import vague_search_price, vague_search_harddrive,vague_search_hdType

from backend.vagueFunctions import vague_search_price, vague_search_harddrive,vague_search_range,vague_search_value,alexa_functions, vague_search_freetext
from backend.binaryFunctions import binary_search_text, binary_search
from backend.helper import Backend_Helper

from backend.addMatchedInformation.add_Matched_Information import ColorInformation
from backend.sortByPriceSameVagunessScore.sort_by_price_same_vaguness_score import SortByPrice
from backend.vagueFunctions.vague_search_price import VagueSearchPrice

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
app = Flask(__name__) #Create the flask instance, __name__ is the name of the current Python module


@app.route('/api/search/alexa', methods=['POST'])
def alexa_search():

    data = request.get_json()
    intent = data["intent"]
    intent_variable = data["intentVariable"]
    intent_variable_value = data[data["intentVariable"]][data["intentVariable"]+"Value"]
    #TODO: boolean method for intentVariable
    #TODO: delete intentVariable with its Value
    del data[intent_variable][intent_variable+"Value"]

    data[intent_variable].update({"intent":intent,"value":intent_variable_value})

    data[intent_variable]["weight"] = 100

    del data["intent"]
    del data["intentVariable"]

    allDocs = es.search(index="amazon", body={
                                                "size": 10000,
                                                "query": {
                                                    "match_all": {}
                                                    }
                                                })

    outputProducts = do_query(data,allDocs)

    return jsonify(outputProducts)


@app.route('/api/search', methods=['POST'])
def search():


    data = request.get_json()

    allDocs = es.search(index="amazon", body={
                                                "size": 10000,
                                                "query": {
                                                    "match_all": {}
                                                    }
                                                })


    outputProducts = do_query(data,allDocs)



    #print("----------------------------------------------------------------")
    #print(outputProducts[47])


    return jsonify(outputProducts)


@app.route('/api/searchText', methods=['POST'])
def searchText():
  data = request.get_json()
  print(data)
  query = data['searchValue']
  outputProducts =[]
  allDocs = es.search(index="amazon", body={
    "size": 10000,
    "query": {
      "match_all": {}
    }
  })
  free_text_searcher =vague_search_freetext.VagueFreeText(es)
  res_search= free_text_searcher.compute_vague_freetext(allDocs, query, False) #False => not boolean search
  #print(res_search)


  outputProducts = Backend_Helper.refineResult(res_search)
  for item in outputProducts: #binary search results all have a vagueness score of 1
    item['vaguenessScore'] =1 #todo: change vagueness score to reflect score
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

    outputProducts = Backend_Helper.refineResult(allDocs)
    return jsonify(outputProducts) #original from alfred


def do_query(data, allDocs):
  #print(data)
  clean_data1 = Backend_Helper.clean_frontend_json(data)
  print("clean_data")
  print(clean_data1)

  #create binary clean data if weighting is equal to 5
  binary_clean_data = {}
  clean_data = {}
  #bool_search_default = False #If no weighting = 5 for any value, do not caculate boolean search below

  for field in clean_data1.keys():
    if clean_data1[field]['weight'] == 5:
      #bool_search_default = True
      binary_clean_data[field] = clean_data1[field] #weigth doesn't matter for boolean search
    else:
      clean_data[field] = clean_data1[field]
      # binary_clean data has to also contain the empty/meaningless fields  because this is the format needed for BinarySearch() method
      # This doesn't matter though because weight has no meaning for boolean search and is not used in the calculation for the result set
      binary_clean_data[field] = {'weight':1}


  #Compute boolean/binary search for items with weighting = 5
  bin_obj = binary_search.BinarySearch()
  query = bin_obj.createBinarySearchQuery(binary_clean_data)
  res = es.search(index="amazon", body=query)
  output_binary = Backend_Helper.refineResult(res)

  print("output Binary")
  print(output_binary) #should be all attributes if no attribute has weight 5

  res_search = list()

  # field_value_dict has the form:
  # {'binary' : { 'brandName': ['acer', 'hp'], 'weight':1}, ...}, 'vague' : {....},
  field_value_dict = extract_fields_and_values(clean_data)
  print(field_value_dict)

  #Get total cumulative weight cum_weight (for example for all attributes weights were 7) and dividue each score by this cum_weight
  cum_weight = 0
  for field_type in field_value_dict.keys():
    for field_name in field_value_dict[field_type]:
      field_weight = field_value_dict[field_type][field_name]["weight"]
      if field_weight != 5: ##Shouldn't happen though because they have already been removed from clean_data
        cum_weight += field_weight




  #todo: erase attributes from field_value_dict that are boolean/weight =5

  # --------------------------------------------------------------------#
  # Objects for each class to use the vague searching functions
  range_searcher = vague_search_range.VagueSearchRange(es)

  binary_searcher = binary_search_text.BinarySearchText(es)

  harddrive_searcher = vague_search_harddrive.VagueHardDrive(es)

  value_searcher = vague_search_value.VagueSearchValue(es)

  price_searcher = vague_search_price.VagueSearchPrice(es)

  alexa_searcher = alexa_functions.AlexaSearch(es)

  # --------------------------------------------------------------------#
  # # Special case to handle hardDriveSize, length is >1 if it has values other than weight

  if 'hardDriveSize' in clean_data and len(clean_data["hardDriveSize"]) > 1:
    res_search += vague_search_harddrive.computeVagueHardDrive_alternative(allDocs, clean_data,
                                                                                          harddrive_searcher,
                                                                                          res_search)
  #  --------------------------------------------------------------------#
  # Special case to handle price

  if 'price' in clean_data and len(clean_data["price"]) > 1:
    res_search += vague_search_price.VagueSearchPrice.computeVaguePrice_alternative(allDocs, clean_data, price_searcher, res_search)

  # --------------------------------------------------------------------#
  # Gets scores for all other attributes
  res_search += call_responsible_methods(allDocs, field_value_dict, range_searcher, binary_searcher, value_searcher,
                                         alexa_searcher)

  # --------------------------------------------------------------------#
  # resList is a list containing a dictionary of ASIN: score values
  # resList = [dict(x) for x in (resVagueListPrice, resVagueListHardDrive)]
  resList = [dict(x) for x in res_search]

  # Counter objects count the occurrences of objects in the list...
  count_dict = Counter()
  for tmp in resList:
    count_dict += Counter(tmp)

  ####new from beshoy
  # convert counter to dictionary
  result = dict(count_dict)
  print("result")
  print(result)
  sortedDict = collections.OrderedDict(sorted(result.items(), key=lambda x: x[1], reverse=True))
  print("sortedDict")
  print(sortedDict)
  # get the keys(asin values)
  asinKeys = list(result.keys())
  # print("asinKeys")
  # print(asinKeys)

  # call the search function
  outputProducts = getElementsByAsin(asinKeys) #calls helper class method refineResuls

  # Compare outputProducts and output_binary to select only items that also occur in boolean search
  outputProducts, output_binary = filter_from_boolean(outputProducts, output_binary)

  # add a vagueness score to the returned objects
  for item in outputProducts:
    print(item['asin'])
    # Normalize the scores so that for each score x,  0< x <=1
    item['vaguenessScore'] = result[item['asin']]/cum_weight

  outputProducts = sorted(outputProducts, key=lambda x: x["vaguenessScore"], reverse=True)

  for item in output_binary: #binary search results that did not meet other vague requirements
    item['vaguenessScore'] =0

  # concatenate with products with weighting 5 *******
  outputProducts = outputProducts + output_binary

  # products with same vagueness score should be listed according to price descending
  c_i = ColorInformation(data, outputProducts, VagueSearchPrice.price_scores)
  searchedValues = c_i.extractKeyValuePairs()
  c_i.prozessDataBinary(searchedValues)

  print(outputProducts[0])

  # If possible, apply sorting before weigthing, so it does not interfere with the list sorted by weighting
  s_p = SortByPrice()
  outputProducts = s_p.sort_by_price(outputProducts)
  return outputProducts


def filter_from_boolean(outputProducts, output_binary):
  count_asin_in_list = []
  for item in outputProducts + output_binary:
    count_asin_in_list.append(item['asin'])

  counter = collections.Counter(count_asin_in_list)
  duplicate_list = []  # list of duplicate items in concatenated list
  for key, value in counter.items():
    if value > 1:
      duplicate_list.append(key)

  #print("duplicate_list")
  #print(duplicate_list)

  # copy only items that are in both lists
  outputProducts = [item for item in outputProducts if item['asin'] in duplicate_list]
  #erase duplicates from output_binary
  output_binary = [item for item in output_binary if item['asin'] not in duplicate_list]

  return outputProducts , output_binary




def callAttributeMethod(attributeName, attributeValue, attributeWeight, allDocs):
  methodName = "computeVague" + attributeName[0].upper() + attributeName[1:]
  className = "vague_search_" + attributeName

  eval(className + "." + methodName)


def extract_fields_and_values(fieldNameToValueDict):
  result = dict(dict())
  result["binary"] = {}
  result["vague"] = {}
  result["range"] = {}
  result["alexa"] = {}

  for fieldName in fieldNameToValueDict:

    if not fieldNameToValueDict[fieldName]:
      continue
    # normal match
    # Ranged terms, example : ram : { minRam : 2,maxRam : 4}
    # If that's the case, then search for minRam and maxRam in fieldNameToValueDict, get them and add range to the query
    value_field_name = fieldName + "Value"
    if type(fieldNameToValueDict[fieldName]) is dict and (
      "minValue" in fieldNameToValueDict[fieldName] or "maxValue" in fieldNameToValueDict[fieldName]):
      # Extract name of field, and set the name of min and max values to minField and maxField, example : minRam and maxRam.
      # Extract the values of minField and maxField from the JSON coming from the front end
      if "minValue" in fieldNameToValueDict[fieldName] and "maxValue" in fieldNameToValueDict[fieldName]:
        result["range"].update({fieldName: {"minValue": fieldNameToValueDict[fieldName]["minValue"]
          , "maxValue": fieldNameToValueDict[fieldName]["maxValue"]
          , "weight": fieldNameToValueDict[fieldName]["weight"]}})

      elif "minValue" in fieldNameToValueDict[fieldName]:
        result["range"].update({fieldName: {"minValue": fieldNameToValueDict[fieldName]["minValue"],
                                            "weight": fieldNameToValueDict[fieldName]["weight"]}})

      elif "maxValue" in fieldNameToValueDict[fieldName]:
        result["range"].update({fieldName: {"maxValue": fieldNameToValueDict[fieldName]["maxValue"],
                                            "weight": fieldNameToValueDict[fieldName]["weight"]}})

    # --------------------------------------------------------------------------------------------------------------------------------#
    # In case of multiple values for the same field, example : ram : [2,4,6], ram is either 2, 4 or 6.
    elif value_field_name in fieldNameToValueDict[fieldName]:
      if type(fieldNameToValueDict[fieldName][value_field_name]) is list:
        if type(fieldNameToValueDict[fieldName][value_field_name][0]) is str:
          fieldNameToValueDict[fieldName][value_field_name] = [x.lower() for x in
                                                               fieldNameToValueDict[fieldName][value_field_name]]
          result["binary"].update({fieldName: {"value": fieldNameToValueDict[fieldName][value_field_name],
                                               "weight": fieldNameToValueDict[fieldName]["weight"]}})
        # --------------------------------------------------------------------------------------------------------------------------------#
        elif type(fieldNameToValueDict[fieldName][value_field_name][0]) is int or type(
          fieldNameToValueDict[fieldName][value_field_name][0]) is float:
          result["vague"].update({fieldName: {"value": fieldNameToValueDict[fieldName][value_field_name],
                                              "weight": fieldNameToValueDict[fieldName]["weight"]}})
        # --------------------------------------------------------------------------------------------------------------------------------#
        # Example : match "{ ram :{"value": 8}}"
      elif type(fieldNameToValueDict[fieldName][value_field_name]) is int or type(
        fieldNameToValueDict[fieldName][value_field_name]) is float:
        result["vague"].update({fieldName: {"value": [fieldNameToValueDict[fieldName][value_field_name]],
                                            "weight": fieldNameToValueDict[fieldName]["weight"]}})
      # --------------------------------------------------------------------------------------------------------------------------------#
      # A normal string match as brandName or hardDriveType
      else:
        # Example : match "{ hardDriveType :{"value": "ssd"}}"
        result["binary"].update({fieldName: {"value": [fieldNameToValueDict[fieldName][value_field_name]],
                                             "weight": fieldNameToValueDict[fieldName]["weight"]}})
      # --------------------------------------------------------------------------------------------------------------------------------#
      # A Query coming from alexa, with only more or less
    elif type(fieldNameToValueDict[fieldName]) is dict and ("intent" in fieldNameToValueDict[fieldName]):
      # Extract name of field, and set the name of min and max values to minField and maxField, example : minRam and maxRam.
      # Extract the values of minField and maxField from the JSON coming from the front end
      result["alexa"].update({fieldName: {"intent": fieldNameToValueDict[fieldName]["intent"],
                                          "value": fieldNameToValueDict[fieldName]["value"],
                                          "weight": fieldNameToValueDict[fieldName]["weight"]}})
  return result


def call_responsible_methods(allDocs, field_value_dict, range_searcher, binary_searcher, value_searcher,
                             alexa_searcher):
  res_search = list()
  # --------------------------------------------------------------------#
  # Extracts each field and its value and weight to the dict
  for field_type in field_value_dict.keys():
    print("field_type")
    print(field_type)

    for field_name in field_value_dict[field_type]:
      if field_name != "price" and field_name != "hardDriveSize":
        field_weight = field_value_dict[field_type][field_name]["weight"]
        # Values for binary key in the dict, these will be searched in the binary_searcher
        if field_type is "binary":
          field_value = field_value_dict[field_type][field_name]["value"]
          res_search.append(binary_searcher.compute_binary_text(field_name, field_weight, field_value))

        # --------------------------------------------------------------------#
        # Values for range key in the dict, these will be searched in the range_searcher
        elif field_type is "range":
          if "minValue" in field_value_dict[field_type][field_name] and "maxValue" in field_value_dict[field_type][
            field_name]:
            min_value = field_value_dict[field_type][field_name]["minValue"]
            max_value = field_value_dict[field_type][field_name]["maxValue"]
            res_search.append(
              range_searcher.compute_vague_range(allDocs, field_name, field_weight, min_value, max_value))

          elif "minValue" in field_value_dict[field_type][field_name]:
            min_value = field_value_dict[field_type][field_name]["minValue"]
            res_search.append(range_searcher.compute_vague_range(allDocs, field_name, field_weight, min_value, None))

          elif "maxValue" in field_value_dict[field_type][field_name]:
            max_value = field_value_dict[field_type][field_name]["maxValue"]
            res_search.append(range_searcher.compute_vague_range(allDocs, field_name, field_weight, None, max_value))
        # --------------------------------------------------------------------#
        # Values for binary key in the dict, these will be searched in the value_searcher
        elif field_type is "vague":
          field_value = field_value_dict[field_type][field_name]["value"]
          res_search.append(value_searcher.compute_vague_value(allDocs, field_name, field_weight, field_value))
        # --------------------------------------------------------------------#
        # Values for alexa
        elif field_type is "alexa":
          field_value = field_value_dict[field_type][field_name]["value"]
          field_intent = field_value_dict[field_type][field_name]["intent"]
          res_search.append(alexa_searcher.compute_boolean_value(field_name, field_weight, field_value, field_intent))
  return res_search

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
  return Backend_Helper.refineResult(result)


if __name__ == "__main__":
    app.run(port=5001, debug=True)
