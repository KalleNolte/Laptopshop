import skfuzzy as fuzz
import numpy as np

class VagueHardDriveType():
  def __init__(self, es):
    self.es = es

  def computeVagueHardDriveType(self, allDocs, hardDriveType):

      body = {
          "query": {
              "bool": {
                  "must": [
                      {"match": {
                          "hardDriveType": hardDriveType
                      }}
                  ]

              }

          },
          "size": 1000
      }

      res = self.es.search(index="amazon", body=body)


      result = []
      for hit in res['hits']['hits']:

          if hit['_source']['hardDriveType']:
              result.append((hit['_source']['asin'], 1))


      # just return the first 100 element(i think 1000 is just too many, but we can change it later)
      # result = result[:100]
      # print("print result of computeVagueHardDriveFunction")
      # print(result)
      return result


