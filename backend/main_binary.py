from flask import Flask, jsonify, render_template, request
from elasticsearch import Elasticsearch
import skfuzzy as fuzz
import numpy as np
from collections import Counter
import json
from collections import defaultdict


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
app = Flask(__name__) #Create the flask instance, __name__ is the name of the current Python module



@app.route('/api/search', methods=['POST'])
def searchBinary():
    data = request.get_json()
    query = createBinarySearchQuery(data)
    res = es.search(index="amazon", body=query)
    #print(res)
    return jsonify(res)



def createBinarySearchQuery(fieldNameToValueDict) :
    body = defaultdict(lambda: defaultdict(lambda : defaultdict(lambda: defaultdict(dict))))

    terms = []
    ranges = []
    sameFieldMultpleValues = []

    for fieldName in fieldNameToValueDict :

        #normal match
        #Ranged terms, example : ram : { minRam : 2,maxRam : 4}
        #If that's the case, then search for minRam and maxRam in fieldNameToValueDict, get them and add range to the query
        if type(fieldNameToValueDict[fieldName]) is dict:
            #Extract name of field, and set the name of min and max values to minField and maxField, example : minRam and maxRam.
            #minValueName = "min"+fieldName[0].upper()+fieldName[1:]
            #maxValueName = "max"+fieldName[0].upper()+fieldName[1:]

            #Extract the values of minField and maxField from the JSON coming from the front end
            minValue = fieldNameToValueDict[fieldName]["minValue"]
            maxValue = fieldNameToValueDict[fieldName]["maxValue"]

            ranges.append({"range" : {fieldName : {"lte" : maxValue,"gte" : minValue }}})

        #--------------------------------------------------------------------------------------------------------------------------------#
        #In case of multiple values for the same field, example : ram : [2,4,6], ram is either 2, 4 or 6.
        elif type(fieldNameToValueDict[fieldName]) is list :
            if type(fieldNameToValueDict[fieldName][0]) is str :
                fieldNameToValueDict[fieldName] = [x.lower() for x in fieldNameToValueDict[fieldName]]
            sameFieldMultpleValues.append({"terms" : {fieldName :fieldNameToValueDict[fieldName] }})
        #--------------------------------------------------------------------------------------------------------------------------------#
        #A normal numerical match, example : ram : 8, ram is 8
        elif type(fieldNameToValueDict[fieldName]) is int or type(fieldNameToValueDict[fieldName]) is float :
            terms.append({"term" : {fieldName : fieldNameToValueDict[fieldName]}})
        #--------------------------------------------------------------------------------------------------------------------------------#
        #A normal string match as brandName or hardDriveType
        else :
            #Example : match "{ ram : 8}"
            terms.append({"term" : {fieldName : fieldNameToValueDict[fieldName].lower()}})
        #--------------------------------------------------------------------------------------------------------------------------------#

    body["query"]["bool"]["must"] = []
    if len(terms) > 0 :
        body["query"]["bool"]["must"].append(terms)
    if len(ranges) > 0 :
        body["query"]["bool"]["must"].append(ranges)
    if len(sameFieldMultpleValues) > 0 :
        body["query"]["bool"]["must"].append(sameFieldMultpleValues)

    body.update({"size":100})

    print(json.dumps(body))


    return body


if __name__ == "__main__":
    app.run(debug=True)
