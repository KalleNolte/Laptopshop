import skfuzzy as fuzz
import numpy as np

class VagueSearchPrice():

  def __init__(self, es):
        self.es = es


  def computeVaguePrice(self, allDocs, minPrice, maxPrice):

    allPrices = []
    for doc in allDocs['hits']['hits']:
      allPrices.append(float(doc['_source']['price']))

    allPrices = np.sort((np.array(allPrices)))
    # print("allPrices: ", allPrices)
    lowerSupport = float(minPrice) - ((float(minPrice) - allPrices[0]) / 2)
    upperSupport = float(maxPrice) + ((allPrices[-1] - float(maxPrice)) / 2)
    # print("lowerSupport: ", lowerSupport)
    # print("upperSupport: ", upperSupport)

    trapmf = fuzz.trapmf(allPrices, [lowerSupport, float(minPrice), float(maxPrice), upperSupport])

    body = {
      "query": {
        "range": {
          "price": {
            "gte": lowerSupport,  # elastic search gte operator = greater than or equals
            "lte": upperSupport  # elastic search lte operator = less than or equals
          }
        }
      }
    }

    # size in range queries should be as many as possible, because when the difference upperSupport and lowerSupport is big, we can lose some products
    # (whose price actually between the minPrice and maxPrice) because we just want to get the first 100 element
    res = self.es.search(index="amazon", body=body, size=1000)

    result = []
    for hit in res['hits']['hits']:
      result.append([hit['_source']['asin'],  # hit['_source']['price'],
                     fuzz.interp_membership(allPrices, trapmf, float(hit['_source']['price']))])


    result = np.array(result, dtype=object)
    result = result[np.argsort(-result[:, 1])]
    # just return the first 100 element(i think 1000 is just too many, but we can change it later)
    result = result[:100]
    result = list(map(tuple, result))
    # print(result)
    return result
