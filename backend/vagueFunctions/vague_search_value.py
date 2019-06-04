import skfuzzy as fuzz
import numpy as np

class VagueSearchValue():

  def __init__(self, es):
        self.es = es


  def compute_vague_value(self, allDocs, fieldName,weight,values):
    allValues = []
    for doc in allDocs['hits']['hits']:
      if (doc['_source'][fieldName]) :
          allValues.append(float(doc['_source'][fieldName]))

    allValues = np.sort((np.array(allValues)))
    # print("allPrices: ", allPrices)
    result = []
    for value in values :
        lowerSupport = float(value) - ((float(value) - allValues[0]) / 2)
        upperSupport = float(value) + ((allValues[-1] - float(value)) / 2)

        trimf = fuzz.trimf(allValues, [lowerSupport, float(value), upperSupport])

        body = {
          "query": {
            "range": {
              fieldName: {
                "gte": lowerSupport,  # elastic search gte operator = greater than or equals
                "lte": upperSupport  # elastic search lte operator = less than or equals
              }
            }
          }
        }

        # size in range queries should be as many as possible, because when the difference upperSupport and lowerSupport is big, we can lose some products
        # (whose price actually between the minPrice and maxPrice) because we just want to get the first 100 element
        res = self.es.search(index="amazon", body=body, size=10000)

        for hit in res['hits']['hits']:
          result.append([hit['_source']['asin'],  # hit['_source']['price'],
                        weight * fuzz.interp_membership(allValues, trimf, float(hit['_source'][fieldName]))])

    result = np.array(result, dtype=object)
    result = result[np.argsort(-result[:, 1])]
    # just return the first 100 element(i think 1000 is just too many, but we can change it later)
    # result = result[:100]
    result = list(map(tuple, result))
    # print(result)
    return result
