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
          print("print hits")
          print(hit)
          result.append([hit['_source']['asin'], float(1.0)])


      print("what is in \"result\"")
      print(result)
      result = np.array(result, dtype=object)
      print("what is in \"result\" with objects") #why?
      print(result)
      # result = result[np.argsort(-result[:, 1])] #sorts resuls with highest matching score first
      # print("what is in \"result\" with objects")  # why?
      # print(result)

      ##
      result = list(map(tuple, result))
      print("result after mapping")
      print(result)
      return result

