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

    # print(result)
    # print(len(result))


    # the result have lots of redundant products with different scores because we passed more than one value
    # for example if ram =[3,4] was searched for
    # maybe there is a product with ram 6 that will get a score say 0.5 from the value ram=3
    # plus it will have another score say 0.7 from the other value (ram = 4)
    unique_result = []

    # o is the number of redundant products for testing purposes
    # o=0

    i=0
    while i < len(result):
        p = i+1
        # a list to get all the scores for one product per iteration
        redundant = []
        while p < len(result):
            # if two products have the same asin
            if result[i][0] == result[p][0]:
              # testing
              # o +=1
              # print(result[p][0])
              # print(result[p][1])
              # print(result[i][0])
              # print(result[i][1])

              # add the score to the redundant list
              redundant.append(result[p][1])
              # then remove this element from the list (so we won't count once more)
              result.remove(result[p])
            p+=1
        # at the end of each iteration we add the score of the proudct from the first loop
        redundant.append(result[i][1])
        # add the product to new list with the max score ( from all the scores we collected so far)
        unique_result.append([result[i][0], max(redundant)])
        i+=1


    # print(o)
    unique_result = np.array(unique_result, dtype=object)
    unique_result = unique_result[np.argsort(-unique_result[:, 1])]
    # just return the first 100 element(i think 1000 is just too many, but we can change it later)
    # result = result[:100]
    unique_result = list(map(tuple, unique_result))
    # print(unique_result)
    # print(len(unique_result))
    return unique_result
