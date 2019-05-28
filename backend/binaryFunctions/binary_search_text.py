import numpy as np

class BinarySearchText:

    def __init__(self, es):
        self.es = es

    def compute_binary_brand(self, text):
        #The following is a case insensitive search
        body = {
                  "query":{
                    "bool":{
                      "must":[
                        {
                          "match":{
                            "brandName": text
                          }
                        }]

                    }
                  }
                }


        res = self.es.search(index="amazon", body=body)
        ###

        result = []
        # Add list including [asin, fuzzycalc] to result. Fuzzy Calculation is between 0 and 1
        for hit in res['hits']['hits']:
            #print("print hits")
            #print(hit)
            result.append([hit['_source']['asin'], float(1.0)])

        #print("what is in \"result\"")
        #print(result)
        result = np.array(result, dtype=object)
        #print("what is in \"result\" with objects")  # why?
        #print(result)
        # result = result[np.argsort(-result[:, 1])] #sorts resuls with highest matching score first
        # print("what is in \"result\" with objects")  # why?
        # print(result)

        ##
        result = list(map(tuple, result))
        #print("result after mapping")
        #print(result)
        return result

    def compute_binary_text(self, data):
        for k, v in data.items():

            #The following is a case insensitive search
            body = {
                      "query":{
                        "bool":{
                          "must":[
                            {
                              "match":{
                                k: v
                              }
                            }]

                        }
                      }
                    }


            res = self.es.search(index="amazon", body=body, size=10000)


            result = []
            # Add list including [asin, fuzzycalc] to result. Fuzzy Calculation is between 0 and 1
            for hit in res['hits']['hits']:
                #print("print hits")
                #print(hit)
                result.append([hit['_source']['asin'], float(1.0)])

            #print("what is in \"result\"")
            #print(result)
            result = np.array(result, dtype=object)
            #print("what is in \"result\" with objects")  # why?
            #print(result)
            # result = result[np.argsort(-result[:, 1])] #sorts resuls with highest matching score first
            # print("what is in \"result\" with objects")  # why?
            # print(result)

            ##
            result = list(map(tuple, result))
            #print("result after mapping")
            #print(result)
            return result

