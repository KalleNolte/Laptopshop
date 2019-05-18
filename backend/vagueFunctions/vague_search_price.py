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
      },
      "size": 10,
    }

    res = self.es.search(index="amazon", body=body)

    result = []
    for hit in res['hits']['hits']:
      result.append([hit['_source']['asin'],  # hit['_source']['price'],
                     fuzz.interp_membership(allPrices, trapmf, float(hit['_source']['price']))])

    # print(result)
    result = np.array(result, dtype=object)
    result = result[np.argsort(-result[:, 1])]
    result = list(map(tuple, result))
    # print(result)
    return result
