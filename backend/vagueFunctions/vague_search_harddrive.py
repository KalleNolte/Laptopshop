import skfuzzy as fuzz
import numpy as np


def computeVagueHardDrive(es, allDocs, hardDriveSize):

    allHardDrives = []
    for doc in allDocs['hits']['hits']:
          if doc['_source']['hddSize'] and doc['_source']['hddSize'] != 0:
              allHardDrives.append(int(doc['_source']['hddSize']))
          if doc['_source']['ssdSize'] and doc['_source']['ssdSize'] != 0:
              allHardDrives.append(int(doc['_source']['ssdSize']))


    # print(allHardDrives)

    allHardDrives = np.sort((np.array(allHardDrives)))
    #("allHardDrives: ", allHardDrives)
    lowerSupport = float(hardDriveSize) - ((float(hardDriveSize) - allHardDrives[0]) / 2)
    upperSupport = float(hardDriveSize) + ((allHardDrives[-1] - float(hardDriveSize)) / 2)
    #print("lowerSupport: ", lowerSupport)
    #print("upperSupport: ", upperSupport)

    trimf = fuzz.trimf(allHardDrives, [lowerSupport, float(hardDriveSize), upperSupport])

    # body = {
    #     "query": {
    #         "bool": {
    #             "must": {
    #                 "match": {
    #                     "hardDriveType": hardDriveType
    #                     }
    #             },
    #             "filter": {
    #                 "range": {
    #                     hardDriveType + "Size": {
    #                         "gte": lowerSupport,
    #                         "lte":upperSupport
    #                     }
    #                 }
    #             }
    #         }
    #     },
    #     "size":10,
    # }

    body = {
        "query": {
            "bool": {
                "should": [
                    {"range": {
                        "hddSize": {
                          "gte": lowerSupport,
                          "lte": upperSupport
                        }
                    }},
                    {"range": {
                        "ssdSize": {
                          "gte": lowerSupport,
                          "lte": upperSupport
                        }
                    }}
                ]
            }
        },
        "size": 10,
    }
    res = es.search(index="amazon", body=body)

    result = []
    for hit in res['hits']['hits']:
        if hit['_source']['hddSize'] and hit['_source']['hddSize'] != 0:
            result.append([hit['_source']['asin'],# hit['_source']['hardDrive'],
                       fuzz.interp_membership(allHardDrives, trimf, float(hit['_source']['hddSize']))])
        # if hit['_source']['ssdSize'] and hit['_source']['ssdSize'] != 0:
        #     result.append([hit['_source']['asin'],# hit['_source']['hardDrive'],
        #                fuzz.interp_membership(allHardDrives, trimf, float(hit['_source']['ssdSize']))])

    print(result)
    result = np.array(result, dtype=object)
    result = result[np.argsort(-result[:, 1])]
    result = list(map(tuple, result)) # turn list of list pairs into list of tuple pairs containting (ASIN, score) pairs
    # print("print result of computeVagueHardDriveFunction")
    # print(result)
    return result
