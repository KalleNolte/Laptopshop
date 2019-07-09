import skfuzzy as fuzz
import numpy as np

class VagueSearchPrice():

  ###########################################-added
  # Used for matched class, to calculate threshhold
  price_scores = {}

  def __init__(self, es):
        self.es = es

  def computeVaguePrice(self, allDocs,weight, minPrice, maxPrice):

    allPrices = []
    for doc in allDocs['hits']['hits']:
      allPrices.append(float(doc['_source']['price']))

    allPrices = np.sort((np.array(allPrices)))
    # print("allPrices: ", allPrices)
    # OLD VERSION
    #lowerSupport = float(minPrice) - ((float(minPrice) - allPrices[0]) / 2)
    #upperSupport = float(maxPrice) + ((allPrices[-1] - float(maxPrice)) / 2)
    # NEW VERSION
    if minPrice is None :
        minPrice = allPrices[0]
    if maxPrice is None:
        maxPrice = allPrices[-1]

    lowerSupport = float(minPrice) - (float(maxPrice) - float(minPrice))
    upperSupport = float(maxPrice) + float(maxPrice) - float(minPrice)

    if minPrice == 0:
        lowerSupport = 0

    #print(allPrices[0])

    trapmf = fuzz.trapmf(allPrices, [lowerSupport, float(minPrice), float(maxPrice), upperSupport])

    body = {
      "query": {
        "range": {
          "price": {
            "gte": lowerSupport,  # elastic search gte operator = greater than or equals
            "lte": upperSupport  # elastic search lte operator = less than or equals
          }
        }
      },"sort": {"price": {"order": "asc"}}
    }

    print(body)

    # size in range queries should be as many as possible, because when the difference upperSupport and lowerSupport is big, we can lose some products
    # (whose price actually between the minPrice and maxPrice) because we just want to get the first 100 element
    res = self.es.search(index="amazon", body=body, size=10000)

    result = []
    for hit in res['hits']['hits']:
      result.append([hit['_source']['asin'],  # hit['_source']['price'],
                     weight*fuzz.interp_membership(allPrices, trapmf, float(hit['_source']['price']))])


    result = np.array(result, dtype=object)
    #result2 = result[np.argsort(result[:])]
    result = result[np.argsort(-result[:, 1])]

    #print("is there an element with vagueness 0?: ", result[:-1])
    # just return the first 100 element(i think 1000 is just too many, but we can change it later)
    #result = result[:100]
    result = list(map(tuple, result))

    ###########################################-added
    # Used for matched class, to calculate threshhold
    VagueSearchPrice.price_scores = result

    return result

  #Added the argument searchedValues
  def computeVaguePrice_alternative(self,allDocs, clean_data,   price_searcher, res_search):
    #if 'price' in clean_data and len(clean_data["price"]) > 1:
    price_weight = clean_data["range"]['price']["weight"]
    if "range" in clean_data["range"]["price"]:
        for range in clean_data["range"]["price"]["range"] :
            if "minValue" in range and "maxValue" in range:
              min_value = range["minValue"]
              max_value = range["maxValue"]
              res_search.append(
                price_searcher.computeVaguePrice(allDocs,  price_weight, min_value, max_value))

            elif "minValue" in range:
              min_value = range["minValue"]
              res_search.append(price_searcher.computeVaguePrice(allDocs,  price_weight, min_value, None))

            elif "maxValue" in range:
              max_value = range["maxValue"]
              res_search.append(price_searcher.computeVaguePrice(allDocs,  price_weight, None, max_value))
    return res_search
