import skfuzzy as fuzz
import numpy as np

class VagueHardDrive():
  def __init__(self, es):
        self.es = es

  def computeVagueHardDrive(self, allDocs, hardDriveSize):

      allHardDrives = []
      for doc in allDocs['hits']['hits']:
            if doc['_source']['hddSize'] and doc['_source']['hddSize'] != 0:
                allHardDrives.append(int(doc['_source']['hddSize']))
            if doc['_source']['ssdSize'] and doc['_source']['ssdSize'] != 0:
                allHardDrives.append(int(doc['_source']['ssdSize']))


      #print(allHardDrives)


      allHardDrives = np.sort((np.array(allHardDrives)))
      print("allHardDrives: ", allHardDrives)
      lowerSupport = float(hardDriveSize) - ((float(hardDriveSize) - allHardDrives[0]) / 2)
      upperSupport = float(hardDriveSize) + ((allHardDrives[-1] - float(hardDriveSize)) / 2)
      # print("lowerSupport: ", lowerSupport)
      # print("upperSupport: ", upperSupport)

      trimf = fuzz.trimf(allHardDrives, [lowerSupport, float(hardDriveSize), upperSupport])
      # print('function')
      # print(trimf)

      # body = {
      #     "query": {
      #         "bool": {
      #             "must": {
      #                 "match": {
      #                     "hardDriveType": hardDriveType
      #                     }
      #             },
      #             "filter": {
      #                 "range": {
      #                     hardDriveType + "Size": {
      #                         "gte": lowerSupport,
      #                         "lte":upperSupport
      #                     }
      #                 }
      #             }
      #         }
      #     },
      #     "size":10,
      # }


      body = {
          "query": {
              "bool": {
                  "should": [
                      {"range": {
                          "hddSize": {
                            "gte": lowerSupport,
                            "lte": upperSupport
                          }
                      }},
                      {"range": {
                          "ssdSize": {
                            "gte": lowerSupport,
                            "lte": upperSupport
                          }
                      }}
                  ]
              }
          },
        "size" : 1000
      }
      res = self.es.search(index="amazon", body=body)

      result = []
      for hit in res['hits']['hits']:
          # in case there is two types, we should take the one with the higher score
          if hit['_source']['hddSize'] and hit['_source']['ssdSize']:
              if hit['_source']['hddSize'] != 0 and hit['_source']['ssdSize'] != 0:
                  result.append([hit['_source']['asin'],  # hit['_source']['hardDrive'],
                                 max(fuzz.interp_membership(allHardDrives, trimf, float(hit['_source']['hddSize'])),fuzz.interp_membership(allHardDrives, trimf, float(hit['_source']['ssdSize'])))])
                  continue

          # laptop has only hdd Drive
          elif hit['_source']['hddSize'] and hit['_source']['hddSize'] != 0:
              result.append([hit['_source']['asin'],# hit['_source']['hardDrive'],
                         fuzz.interp_membership(allHardDrives, trimf, float(hit['_source']['hddSize']))])

          # laptop has only ssd Drive
          elif hit['_source']['ssdSize'] and hit['_source']['ssdSize'] != 0:
              result.append([hit['_source']['asin'],# hit['_source']['hardDrive'],
                         fuzz.interp_membership(allHardDrives, trimf, float(hit['_source']['ssdSize']))])


      result = np.array(result, dtype=object)
      result = result[np.argsort(-result[:, 1])]
      result = list(map(tuple, result)) # turn list of list pairs into list of tuple pairs containting (ASIN, score) pairs
      # just return the first 100 element(i think 1000 is just too many, but we can change it later)
      result = result[:100]
      # print("print result of computeVagueHardDriveFunction")
      # print(result)
      return result
