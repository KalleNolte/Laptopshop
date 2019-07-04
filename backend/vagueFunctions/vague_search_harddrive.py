import skfuzzy as fuzz
import numpy as np

class VagueHardDrive():
    def __init__(self, es):
        self.es = es

    def computeVagueHardDrive(self, allDocs,  weight, minValue, maxValue):

      allHardDrives = []
      for doc in allDocs['hits']['hits']:
            if doc['_source']["hddSize"]and doc['_source']['hddSize'] != 0:
                allHardDrives.append(int(doc['_source']['hddSize']))
            if doc['_source']['ssdSize'] and doc['_source']['ssdSize'] != 0:
                allHardDrives.append(int(doc['_source']['ssdSize']))



      allHardDrives = np.sort((np.array(allHardDrives)))


      if maxValue is None :
          maxValue = allHardDrives[-1]
      if minValue is None:
          minValue = allHardDrives[0]


      # in case the user enter the hard Drive size as a range
      lowerSupport = float(minValue) - ((float(minValue) - allHardDrives[0]) / 2)
      upperSupport = float(maxValue) + ((allHardDrives[-1] - float(maxValue)) / 2)
      vagueFunction = fuzz.trapmf(allHardDrives, [lowerSupport, float(minValue), float(maxValue), upperSupport])
      # in case the user enter the hard drive as a single value



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
        "size" : 10000
      }
      res = self.es.search(index="amazon", body=body)

      result = []
      for hit in res['hits']['hits']:
          # in case there is two types, we should take the one with the higher score
          if hit['_source']['hddSize'] and hit['_source']['ssdSize']:
              if hit['_source']['hddSize'] != 0 and hit['_source']['ssdSize'] != 0:
                  result.append([hit['_source']['asin'],  # hit['_source']['hardDrive'],
                                 weight * max(fuzz.interp_membership(allHardDrives, vagueFunction, float(hit['_source']['hddSize'])),fuzz.interp_membership(allHardDrives, vagueFunction, float(hit['_source']['ssdSize'])))])
                  continue

          # laptop has only hdd Drive
          elif hit['_source']['hddSize'] and hit['_source']['hddSize'] != 0:
              result.append([hit['_source']['asin'],# hit['_source']['hardDrive'],
                         weight * fuzz.interp_membership(allHardDrives, vagueFunction, float(hit['_source']['hddSize']))])

          # laptop has only ssd Drive
          elif hit['_source']['ssdSize'] and hit['_source']['ssdSize'] != 0:
              result.append([hit['_source']['asin'],# hit['_source']['hardDrive'],
                         weight * fuzz.interp_membership(allHardDrives, vagueFunction, float(hit['_source']['ssdSize']))])


      result = np.array(result, dtype=object)
      result = result[np.argsort(-result[:, 1])]
      result = list(map(tuple, result)) # turn list of list pairs into list of tuple pairs containting (ASIN, score) pairs
      # just return the first 100 element(i think 1000 is just too many, but we can change it later)
      #result = result[:100]
      # print("print result of computeVagueHardDriveFunction")
      return result

    def computeVagueHardDrive_alternative(self,allDocs, clean_data, harddrive_searcher, res_search):
      # Special case to handle hardDriveSize, length is >1 if it has values other than weight
      #if 'hardDriveSize' in clean_data and len(clean_data["hardDriveSize"]) > 1:
      hd_size_weight = clean_data["range"]['hardDriveSize']["weight"]
      if "range" in clean_data["range"]["hardDriveSize"]:
          for range in clean_data["range"]["hardDriveSize"]["range"]:
              if "minValue" in range and "maxValue" in range:
                min_value = range["minValue"]
                max_value = range["maxValue"]
                res_search.append(
                  harddrive_searcher.computeVagueHardDrive(allDocs,  hd_size_weight, min_value, max_value)) # Discrete value needed not a range
              elif "minValue" in range:
                min_value = range["minValue"]
                res_search.append(harddrive_searcher.computeVagueHardDrive(allDocs,  hd_size_weight, min_value, None))

              elif "maxValue" in range:
                max_value = range["maxValue"]
                res_search.append(harddrive_searcher.computeVagueHardDrive(allDocs,  hd_size_weight, None, max_value))
      return res_search
