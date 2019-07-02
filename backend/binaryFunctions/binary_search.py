from collections import defaultdict

import numpy as np



class BinarySearch():
  # #classical logic: objects are in set of results (=1) or they are not (=0).
  # def computeBinaryPrice(allDocs, minPrice, maxPrice):
  #
  #     body = {
  #                 "sort": {
  #                   "price": "asc"
  #                 },
  #                 "query": {
  #                     "range" : {
  #                         "price" : {
  #                             "gte" : minPrice,
  #                             "lte" : maxPrice
  #                         }
  #                     }
  #                 }
  #             }
  #     #Get a result of laptops that have price >= minPrice and price<=maxPrice
  #     res = es.search(index="amazon", body=body)
  #     ###
  #
  #     result = []
  #     #Add list including [asin, fuzzycalc] to result. Fuzzy Calculation is between 0 and 1
  #     for hit in res['hits']['hits']:
  #         print("print hits")
  #         print(hit)
  #         result.append([hit['_source']['asin'], float(1.0)])
  #
  #
  #     print("what is in \"result\"")
  #     print(result)
  #     result = np.array(result, dtype=object)
  #     print("what is in \"result\" with objects") #why?
  #     print(result)
  #     # result = result[np.argsort(-result[:, 1])] #sorts resuls with highest matching score first
  #     # print("what is in \"result\" with objects")  # why?
  #     # print(result)
  #
  #     ##
  #     result = list(map(tuple, result))
  #     print("result after mapping")
  #     print(result)
  #     return result
  #
  # #classical logic: objects are in set of results (=1) or they are not (=0).
  # def computeBinaryHarddrive(allDocs, harddrive):
  #
  #     body = {
  #               "query": {
  #                 "match": {
  #                   "hardDrive": harddrive
  #                 }
  #               }
  #             }
  #     #Get a result of laptops that have price >= minPrice and price<=maxPrice
  #     res = es.search(index="amazon", body=body)
  #     ###
  #
  #     result = []
  #     #Add list including [asin, fuzzycalc] to result. Fuzzy Calculation is between 0 and 1
  #     for hit in res['hits']['hits']:
  #         result.append([hit['_source']['asin'], float(1.0)])
  #
  #
  #     print("what is in \"result\"")
  #     print(result)
  #     result = np.array(result, dtype=object)
  #     print("what is in \"result\" with objects") #why?
  #     print(result)
  #     # result = result[np.argsort(-result[:, 1])] #sorts resuls with highest matching score first
  #
  #
  #     ##
  #     result = list(map(tuple, result))
  #     #print(result)
  #     return result

  #classical logic: objects are in set of results (=1) or they are not (=0).
  def computeBinary(es, minPrice, maxPrice, harddrive):

      #change "hardDrive" to "ssdSize" or "hddSize"
      body = {
                "query": {
                  "bool":{
                    "must":[
                      {
                        "match":{
                          "hardDrive": harddrive
                        }
                      },
                      {
                        "range": {
                    "price": {
                      "gte": minPrice,
                      "lte": maxPrice
                              }
                          }
                      }
                      ]

                    }
                  },
                  "sort": {"price": {"order": "asc"}}
                }


      #Get a result of laptops that have price >= minPrice and price<=maxPrice
      res = es.search(index="amazon", body=body)
      ###

      result = []
      #Add list including [asin, fuzzycalc] to result. Fuzzy Calculation is between 0 and 1
      for hit in res['hits']['hits']:

          result.append([hit['_source']['asin'], float(1.0)])



      result = np.array(result, dtype=object)

      # result = result[np.argsort(-result[:, 1])] #sorts resuls with highest matching score first
      # print("what is in \"result\" with objects")  # why?
      # print(result)

      ##
      result = list(map(tuple, result))

      return result

  def createBinarySearchQuery(self, fieldNameToValueDict):
    body = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict))))


    terms = []
    ranges = []
    alexa = []
    sameFieldMultpleValues = []
    hardDriveSizeValues = []

    boolean_ssd_and_hdd = False

    wanted_hdd_type = None

    if "hardDriveSize" in fieldNameToValueDict and len(fieldNameToValueDict["hardDriveSize"].keys()) > 1:

      if "hardDriveType" not in fieldNameToValueDict or fieldNameToValueDict["hardDriveType"].lower() == "hybrid":
        hardDriveSize_value = fieldNameToValueDict["hardDriveSize"]
        del fieldNameToValueDict["hardDriveSize"]
        fieldNameToValueDict.update({"ssdSize": hardDriveSize_value, "hddSize": hardDriveSize_value})
        boolean_ssd_and_hdd = True
      elif fieldNameToValueDict["hardDriveType"].lower() == "ssd":
        hardDriveSize_value = fieldNameToValueDict["hardDriveSize"]
        del fieldNameToValueDict["hardDriveSize"]
        fieldNameToValueDict.update({"ssdSize": hardDriveSize_value})
        wanted_hdd_type = "ssdSize"
      else:
        hardDriveSize_value = fieldNameToValueDict["hardDriveSize"]
        del fieldNameToValueDict["hardDriveSize"]
        fieldNameToValueDict.update({"hddSize": hardDriveSize_value})
        wanted_hdd_type = "hddSize"


    if boolean_ssd_and_hdd:
      # Discrete value with ssd and hdd
      if "hardDriveSizeRange" in fieldNameToValueDict["hddSize"]:

        hdd_ranges = list()

        for range in fieldNameToValueDict["hddSize"]["hardDriveSizeRange"]:
            # ranged value with ssd and hdd
            if "minValue" in range and "maxValue" in range:

              minValue = range["minValue"]
              maxValue = range["maxValue"]
              hdd_ranges.append({"range": {"hddSize": {"lte": maxValue, "gte": minValue}}})
              hdd_ranges.append({"range": {"ssdSize": {"lte": maxValue, "gte": minValue}}})

            elif "minValue" in range :
              minValue = range["minValue"]
              hdd_ranges.append({"range": {"hddSize": {"gte": minValue}}})
              hdd_ranges.append({"range": {"ssdSize": {"gte": minValue}}})


            elif "maxValue" in range:
              maxValue = range["maxValue"]
              hdd_ranges.append({"range": {"hddSize": {"lte": maxValue}}})
              hdd_ranges.append({"range": {"hddSize": {"lte": maxValue}}})
        if len(hdd_ranges) > 0 :
            hardDriveSizeValues.append({"bool" :{"should":hdd_ranges}})
    elif wanted_hdd_type is not None :
        if "hardDriveSizeRange" in fieldNameToValueDict[wanted_hdd_type]:

          for range in fieldNameToValueDict[wanted_hdd_type]["hardDriveSizeRange"]:
              # ranged value with ssd and hdd
              if "minValue" in range and "maxValue" in range:

                minValue = range["minValue"]
                maxValue = range["maxValue"]
                hardDriveSizeValues.append({"range": {wanted_hdd_type: {"lte": maxValue, "gte": minValue}}})

              elif "minValue" in range :
                minValue = range["minValue"]
                hardDriveSizeValues.append({"range": {wanted_hdd_type: {"gte": minValue}}})


              elif "maxValue" in range:
                maxValue = range["maxValue"]
                hardDriveSizeValues.append({"range": {wanted_hdd_type: {"lte": maxValue}}})

    for fieldName in fieldNameToValueDict:

      if not fieldNameToValueDict[fieldName] or fieldName == "ssdSize" or fieldName == "hddSize":
         continue

      # normal match
      # Ranged terms, example : ram : { minRam : 2,maxRam : 4}
      # If that's the case, then search for minRam and maxRam in fieldNameToValueDict, get them and add range to the query
      value_field_name = fieldName + "Value"
      range_field_name = fieldName + "Range"
      if range_field_name in fieldNameToValueDict[fieldName]:
        # Extract name of field, and set the name of min and max values to minField and maxField, example : minRam and maxRam.
        # minValueName = "min"+fieldName[0].upper()+fieldName[1:]
        # maxValueName = "max"+fieldName[0].upper()+fieldName[1:]

        # Extract the values of minField and maxField from the JSON coming from the front end
          field_ranges = list()
          for range in fieldNameToValueDict[fieldName][range_field_name] :
              if "minValue" in range and "maxValue" in range:
                  minValue = range["minValue"]
                  maxValue = range["maxValue"]
                  field_ranges.append({"range": {fieldName: {"lte": maxValue, "gte": minValue}}})

              elif "minValue" in range:
                  minValue = range["minValue"]
                  field_ranges.append({"range": {fieldName: {"gte": minValue}}})

              elif "maxValue" in range:
                  maxValue = range["maxValue"]
                  field_ranges.append({"range": {fieldName: {"lte": maxValue}}})
          if len(field_ranges) > 0 :
              ranges.append({"bool" :{"should":field_ranges}})

      # --------------------------------------------------------------------------------------------------------------------------------#
      # In case of multiple values for the same field, example : ram : [2,4,6], ram is either 2, 4 or 6.
      elif value_field_name in fieldNameToValueDict[fieldName]:
        if type(fieldNameToValueDict[fieldName][value_field_name]) is list:
          if type(fieldNameToValueDict[fieldName][value_field_name][0]) is str:
            fieldNameToValueDict[fieldName] = [x.lower() for x in fieldNameToValueDict[fieldName]]
          sameFieldMultpleValues.append({"terms": {fieldName: fieldNameToValueDict[fieldName][value_field_name]}})
        # --------------------------------------------------------------------------------------------------------------------------------#
        # A normal numerical match, example : ram : 8, ram is 8
        elif type(fieldNameToValueDict[fieldName][value_field_name]) is int or type(
          fieldNameToValueDict[fieldName][value_field_name]) is float:
          terms.append({"term": {fieldName: fieldNameToValueDict[fieldName][value_field_name]}})
        # --------------------------------------------------------------------------------------------------------------------------------#
        # A normal string match as brandName or hardDriveType
        else:
          # Example : match "{ ram : 8}"
          terms.append({"term": {fieldName: fieldNameToValueDict[fieldName][value_field_name].lower()}})
        # --------------------------------------------------------------------------------------------------------------------------------#
      elif type(fieldNameToValueDict[fieldName]) is dict and ("intent" in fieldNameToValueDict[fieldName]):
        # Extract name of field, and set the name of min and max values to minField and maxField, example : minRam and maxRam.
        # Extract the values of minField and maxField from the JSON coming from the front end
        field_intent = fieldNameToValueDict[fieldName]["intent"]
        es_intent = "gt" if field_intent == "more" else "lt"
        ranges.append({"range": {fieldName: {es_intent: fieldNameToValueDict[fieldName]["value"]}}})

    body["query"]["bool"]["must"] = []
    body["query"]["bool"]["should"] = []

    if len(hardDriveSizeValues) > 0:
      body["query"]["bool"]["must"].append(hardDriveSizeValues)
    if len(terms) > 0:
      body["query"]["bool"]["must"].append(terms)
    if len(ranges) > 0:
      body["query"]["bool"]["must"].append(ranges)
    if len(sameFieldMultpleValues) > 0:
      body["query"]["bool"]["must"].append(sameFieldMultpleValues)


    body.update({"size": 10000})

    print(body)

    #print("body", body)
    return body
