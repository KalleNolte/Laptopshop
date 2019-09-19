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

    res = self.es.search(index="amazon", body=body, size=10000)

    result = []
    for hit in res['hits']['hits']:
      result.append([hit['_source']['asin'],  # hit['_source']['price'],
                     weight*fuzz.interp_membership(allPrices, trapmf, float(hit['_source']['price']))])


    result = np.array(result, dtype=object)
    result = result[np.argsort(-result[:, 1])]
    result = list(map(tuple, result))

    ###########################################-added
    # Used for matched class, to calculate threshhold
    VagueSearchPrice.price_scores = result

    return result


  def computeVaguePriceMultiple(self, allDocs, weight, interval_list):
    allPrices = []
    for doc in allDocs['hits']['hits']:
      allPrices.append(float(doc['_source']['price']))

    allPrices = np.sort((np.array(allPrices)))

    query =[]
    fuzzy_logic_results = []
    for i in range(len(interval_list)):
      if interval_list[i]['minValue'] is not None:
        minPrice = interval_list[i]['minValue']
      else:
        minPrice = allPrices[0]

      if interval_list[i]['maxValue'] is not None:
        maxPrice = interval_list[i]['maxValue']
      else:
        maxPrice = allPrices[-1]
      lowerSupport = float(minPrice) - (float(maxPrice) - float(minPrice))
      upperSupport = float(maxPrice) + (float(maxPrice) - float(minPrice))
      # print( "support: ", lowerSupport, upperSupport)
      if minPrice == 0:
        lowerSupport = 0
      query.append({"range": {"price": {"gte": lowerSupport, "lte": upperSupport }}},)
      trapmf = fuzz.trapmf(allPrices, [lowerSupport, float(minPrice), float(maxPrice), upperSupport])
      fuzzy_logic_results.append(trapmf)

    body =     {
      "query": {
        "bool": {
          "should": query
        }
      },
        "sort": {"price": {"order": "asc"}}

    }

    res = self.es.search(index="amazon", body=body, size=10000)

    result = []
    for hit in res['hits']['hits']:
      scores = []
      for score in fuzzy_logic_results:
        score1 =fuzz.interp_membership(allPrices, score, float(hit['_source']['price']))
        scores.append(score1)
      result.append([hit['_source']['asin'],
                     weight * max(scores)])

    result = np.array(result, dtype=object)
    result = result[np.argsort(-result[:, 1])]

    result = list(map(tuple, result))

    ###########################################-added
    # Used for matched class, to calculate threshhold
    VagueSearchPrice.price_scores = result

    return result

  #Added the argument searchedValues
  def computeVaguePrice_alternative(self,allDocs, clean_data,   price_searcher, res_search):
    price_weight = clean_data["range"]['price']["weight"]
    if "range" in clean_data["range"]["price"]:
        # print( clean_data["range"]["price"]["range"] )

        """If interval is one consecutive interval, then search for gte: min_value, lte: max_value"""
        if len( clean_data["range"]["price"]["range"] ) ==1:
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
        else: # multiple intervals
          res_search.append( price_searcher.computeVaguePriceMultiple(allDocs, price_weight,clean_data["range"]["price"]["range"] ))


    return res_search
