from flask import Flask, jsonify, render_template, request
from elasticsearch import Elasticsearch
import skfuzzy as fuzz
import numpy as np
from collections import Counter
import json

from backend.binaryFunctions import binary_search


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
app = Flask(__name__) #Create the flask instance, __name__ is the name of the current Python module
priceDict = {}
hdDict = {}
productTitleDict = {}
allDocs ={}

# @app.route('/search')
# def index():
#     return render_template('main.html')


@app.route('/search', methods=['POST'])
def search():

    minPrice = request.form['minPrice']
    maxPrice = request.form['maxPrice']
    hardDrive = request.form['hardDrive']

    resBinary = binary_search.BinarySearch.computeBinary(es, minPrice, maxPrice, hardDrive)
    resList = [dict(x) for x in (resBinary, )]


    #Counter objects count the occurrences of objects in the list...
    #count_dict contains each object from resList, and sums the scores for all occurrences. So if asin B07.. occurs
    # twice with a score of 1.0, then it has a score of 2.0 in count_dict
    count_dict = Counter()
    for tmp in resList:
        count_dict += Counter(tmp)

    # print("count_dict")
    # print(count_dict)
    # print("dict(count_dict).items()")
    # print(dict(count_dict).items()) #contains pairs

    #count_dict is a dictionary of key/value pairs. Below is a list comprehension (for dictionaries?) to get key k and value v from each pair (k,v)
    outputProducts = [("ASIN: {}".format(k), "Product Title: {}".format(productTitleDict[k]), "Vagueness Score: {}".format(v/2),
                       "Price: {}".format(priceDict[k]), "Hard Drive Size: {}".format(hdDict[k])) for k, v in dict(count_dict).items()]

    outputProducts = sorted(outputProducts, key=lambda x: x[2], reverse=True)

    return jsonify(outputProducts) #original from alfred





if __name__ == "__main__":
    app.run(debug=True)
