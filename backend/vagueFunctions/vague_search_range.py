import skfuzzy as fuzz
import numpy as np

class VagueSearchRange():

  def __init__(self, es):
        self.es = es

  def compute_vague_range_mult_intervals(self, allDocs, fieldName, weight, interval_list):
    """This function takes a list of intervals (dictionaries with min and max), as entered through the checkboxes on the
    website.  For each dictionary with a minimum and maximum range value, calcalate the lower and upper limits.
    Then compose an elastic search which searches for items within the lower and upper limits of any interval (logical OR).

    Calculation of the membership function: A membership function is created for each interval.  A score of 1.0 is given
    to values within the min and max of the interval.  A score between (0,1] is given to a value within the lower boundaries
    and the minimum and between the max and upperboundary.  This score is calculated per interval.

    Calculation of the vagueness Score: For each item in the result list, this function compares the membership function
    result calculation of a vaguessness score and saves the maximum vagueness score for each item.

    :returns vagueness scores"""

    allValues = []
    for doc in allDocs['hits']['hits']:
      if (doc['_source'][fieldName]):
        allValues.append(float(doc['_source'][fieldName]))

    allValues = np.sort((np.array(allValues)))
    query = []
    fuzzy_logic_results = []

    for i in range(len(interval_list)):
      print(interval_list[i]['minValue'])
      if interval_list[i]['minValue'] is not None:
        min = interval_list[i]['minValue']
      else:
        min = allValues[0]

      if interval_list[i]['maxValue'] is not None:
        max = interval_list[i]['maxValue']
      else:
        max = allValues[-1]

      lowerSupport = float(min) - (float(max) - float(min))
      upperSupport = float(max) + float(max) - float(min)
      print("support: ", lowerSupport, upperSupport)
      if min == 0:
        lowerSupport = 0
      query.append({"range": {fieldName: {"gte": lowerSupport, "lte": upperSupport}}}, )
      trapmf = fuzz.trapmf(allValues, [lowerSupport, float(min), float(max), upperSupport])
      fuzzy_logic_results.append(trapmf)

    body = {
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
        score1 = fuzz.interp_membership(allValues, score, float(hit['_source'][fieldName]))
        scores.append(score1)

      if len(scores)>0:
        max_score = scores[0]
        for i in range(len(scores)-1):
          if scores[i]< scores[i+1]:
            max_score = scores[i+1]
        result.append([hit['_source']['asin'], weight * max_score])

    result = np.array(result, dtype=object)
    result = result[np.argsort(-result[:, 1])]
    result = list(map(tuple, result))
    print(result)
    return result

  def compute_vague_range(self, allDocs, fieldName,weight, minValue, maxValue):
    """This function takes a min and max, as entered through the checkboxes on the website if one interval is selected.
    Based on the min and max, calcalate the lower and upper limits.
    Then compose an elastic search which searches for items within the lower and upper limits.

    Calculation of the membership function: =A score of 1.0 is given to values within the min and max of the interval.
    A score between (0,1] is given to a value within the lower boundaries and the minimum and between the max and upper
    boundary.

    Calculation of the vagueness Score: For each item in the result list, this function calculates vagueness score for
    each item.

    :returns vagueness scores"""

    allValues = []
    for doc in allDocs['hits']['hits']:
      if (doc['_source'][fieldName]) :
          allValues.append(float(doc['_source'][fieldName]))

    allValues = np.sort((np.array(allValues)))


    if maxValue is None :
        maxValue = allValues[-1]
    if minValue is None:
        minValue = allValues[0]

    # OLD
    # lowerSupport = float(minValue) - ((float(minValue) - allValues[0]) / 2)
    # upperSupport = float(maxValue) + ((allValues[-1] - float(maxValue)) / 2)
    # NEW
    lowerSupport = float(minValue) - (float(maxValue) - float(minValue))
    upperSupport = float(maxValue) + (float(maxValue) - float(minValue))
    if minValue == 0:
        lowerSupport = 0

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
                    weight *  fuzz.interp_membership(allValues, trapmf, float(hit['_source'][fieldName]))])


    result = np.array(result, dtype=object)
    result = result[np.argsort(-result[:, 1])]
    # just return the first 100 element(i think 1000 is just too many, but we can change it later)
    #result = result[:100]
    result = list(map(tuple, result))
    # print(result)
    return result
