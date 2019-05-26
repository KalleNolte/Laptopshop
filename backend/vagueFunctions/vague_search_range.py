import skfuzzy as fuzz
import numpy as np

class VagueSearchRange():

  def __init__(self, es):
        self.es = es


  def compute_vague_range(self, allDocs, fieldName, minValue, maxValue, weight):

    allValues = []
    for doc in allDocs['hits']['hits']:
      allValues.append(float(doc['_source'][fieldName]))

    allValues = np.sort((np.array(allValues)))
    # print("allPrices: ", allPrices)
    lowerSupport = float(minValue) - ((float(minValue) - allValues[0]) / 2)
    upperSupport = float(maxValue) + ((allValues[-1] - float(maxValue)) / 2)
    # print("lowerSupport: ", lowerSupport)
    # print("upperSupport: ", upperSupport)

    trapmf = fuzz.trapmf(allValues, [lowerSupport, float(minValue), float(maxValue), upperSupport])

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

    result = []
    for hit in res['hits']['hits']:
      result.append([hit['_source']['asin'],  # hit['_source']['price'],
                     fuzz.interp_membership(allValues, trapmf, weight * float(hit['_source'][fieldName]))])


    result = np.array(result, dtype=object)
    result = result[np.argsort(-result[:, 1])]
    # just return the first 100 element(i think 1000 is just too many, but we can change it later)
    result = result[:100]
    result = list(map(tuple, result))
    # print(result)
    return result
