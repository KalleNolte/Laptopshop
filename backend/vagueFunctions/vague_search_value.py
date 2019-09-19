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
    fuzzy_logic_results = []
    support = (allValues[-1]-allValues[0]) /8
    query = []
    for value in values :
        # OLD:
        # lowerSupport = float(value) - ((float(value) - allValues[0]) / 2)
        # upperSupport = float(value) + ((allValues[-1] - float(value)) / 2)
        """ Triangular function is symmetrical if upper and lower boundaries are equally far from the entered value."""
        #NEW:
        if (float(value)- support) > allValues[0]:
          lowerSupport = float(value)- support
        else:
          lowerSupport = allValues[0]
        if (float(value) + support) < allValues[-1]:
          upperSupport = float(value) + support
        else:
          upperSupport = allValues[-1]
        trimf = fuzz.trimf(allValues, [lowerSupport, float(value), upperSupport])
        fuzzy_logic_results.append(trimf)
        print(lowerSupport)

        query.append({"range": {fieldName: {"gte": lowerSupport, "lte": upperSupport}}}, )
        # body = {
        #   "query": {
        #     "range": {
        #       fieldName: {
        #         "gte": lowerSupport,  # elastic search gte operator = greater than or equals
        #         "lte": upperSupport  # elastic search lte operator = less than or equals
        #       }
        #     }
        #   }
        # }

    body = {
      "query": {
        "bool": {
          "should": query
        }
      },
      "sort": {"price": {"order": "asc"}}

    }

    res = self.es.search(index="amazon", body=body, size=10000)

    # for hit in res['hits']['hits']:
    #   result.append([hit['_source']['asin'],  # hit['_source']['price'],
    #                 weight * fuzz.interp_membership(allValues, trimf, float(hit['_source'][fieldName]))])

    for hit in res['hits']['hits']:
      scores = []
      for score in fuzzy_logic_results:
        score1 = fuzz.interp_membership(allValues, score, float(hit['_source']['price']))
        scores.append(score1)
      result.append([hit['_source']['asin'],
                     weight * max(scores)])

    result = np.array(result, dtype=object)
    result = result[np.argsort(-result[:, 1])]
    # just return the first 100 element(i think 1000 is just too many, but we can change it later)


    result = list(map(tuple, result))
    # print(result)
    return result
