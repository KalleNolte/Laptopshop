import skfuzzy as fuzz
import numpy as np

class VagueSearchPrice():

  ###########################################-added
  # Used for matched class, to calculate threshhold
  price_scores = {}

  def __init__(self, es):
        self.es = es

  def computeVaguePrice(self, allDocs,weight, minPrice, maxPrice, searchedValues):

    allPrices = []
    for doc in allDocs['hits']['hits']:
      allPrices.append(float(doc['_source']['price']))

    allPrices = np.sort((np.array(allPrices)))
    # print("allPrices: ", allPrices)
    # OLD VERSION
    #lowerSupport = float(minPrice) - ((float(minPrice) - allPrices[0]) / 2)
    #upperSupport = float(maxPrice) + ((allPrices[-1] - float(maxPrice)) / 2)
    # NEW VERSION
    lowerSupport = float(minPrice) - (float(searchedValues["maxValue"]) - float(searchedValues["minValue"]))
    upperSupport = float(maxPrice) + float(searchedValues["maxValue"]) - float(searchedValues["minValue"])
    print("lowerSupport: ", lowerSupport)
    print("upperSupport: ", upperSupport)
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

    # size in range queries should be as many as possible, because when the difference upperSupport and lowerSupport is big, we can lose some products
    # (whose price actually between the minPrice and maxPrice) because we just want to get the first 100 element
    res = self.es.search(index="amazon", body=body, size=10000)

    result = []
    for hit in res['hits']['hits']:
      result.append([hit['_source']['asin'],  # hit['_source']['price'],
                     weight*fuzz.interp_membership(allPrices, trapmf, float(hit['_source']['price']))])


    result = np.array(result, dtype=object)
    result = result[np.argsort(-result[:, 1])]
    # just return the first 100 element(i think 1000 is just too many, but we can change it later)
    #result = result[:100]
    result = list(map(tuple, result))
    print("result from vague_search_price:", result)

    ###########################################-added
    # Used for matched class, to calculate threshhold
    VagueSearchPrice.price_scores = result

    return result

  #Added the argument searchedValues
  def computeVaguePrice_alternative(allDocs, clean_data,   price_searcher, res_search, searchedValues):
    #if 'price' in clean_data and len(clean_data["price"]) > 1:
    price_weight = clean_data['price']["weight"]
    if "value" in clean_data["price"]:  # Discrete value needed not a range
      price_min = clean_data['price']["value"]
      res_search.append(price_searcher.computeVaguePrice(allDocs, price_weight, price_min, None))
    else:
      price_min = clean_data['price']["minValue"]
      price_max = clean_data['price']["maxValue"]
      #price_weight = clean_data['price']["weight"]
      res_search.append(price_searcher.computeVaguePrice(allDocs, price_weight, price_min, price_max, searchedValues))
      print(searchedValues, "In price Searcher")
    return res_search
