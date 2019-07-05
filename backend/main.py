from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch

#from collections
#from flask_cors import CORS

#
# from vagueFunctions import vague_search_price, vague_search_harddrive,vague_search_range,vague_search_value
# from binaryFunctions import binary_search_text
# from helper import Backend_Helper
# from vagueFunctions import vague_search_price, vague_search_harddrive,vague_search_hdType

#from backend.services_b import do_query
import backend.services_b as service
#from backend.services_b import get_all_documents

from backend.vagueFunctions import vague_search_freetext
from backend.helper import Backend_Helper

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
app = Flask(__name__) #Create the flask instance, __name__ is the name of the current Python module


@app.route('/api/search/alexa', methods=['POST'])
def alexa_search():

    data = request.get_json()
    intent = data["intent"]
    intent_variable = data["intentVariable"]
    intent_variable_value = data[data["intentVariable"]][data["intentVariable"]+"Value"]
    #TODO: boolean method for intentVariable
    #TODO: delete intentVariable with its Value
    del data[intent_variable][intent_variable+"Value"]

    data[intent_variable].update({"intent":intent,"value":intent_variable_value})

    data[intent_variable]["weight"] = 100

    del data["intent"]
    del data["intentVariable"]

    allDocs = service.get_all_documents()

    outputProducts = service.do_query(data, allDocs)

    return jsonify(outputProducts)


@app.route('/api/search', methods=['POST'])
def search():


    data = request.get_json()

    #allDocs = service.get_all_documents()
    #outputProducts = service.do_query(data, allDocs)

    #set serialized object
    service.get_all_documents()
    outputProducts = service.do_query(data)


    return jsonify(outputProducts)


@app.route('/api/searchText', methods=['POST'])
def searchText():
  data = request.get_json()
  #print(data)
  query = data['searchValue']
  outputProducts =[]

  allDocs = service.get_all_documents()

  free_text_searcher =vague_search_freetext.VagueFreeText(es)
  res_search= free_text_searcher.compute_vague_freetext(allDocs, query, False) #False => not boolean search
  #print(res_search)


  outputProducts = Backend_Helper.refineResult(res_search)
  for item in outputProducts: #binary search results all have a vagueness score of 1
    item['vaguenessScore'] =1 #todo: change vagueness score to reflect score
  return jsonify(outputProducts)


@app.route('/api/sample', methods=['GET'])
def getSample():

    allDocs = service.get_test_documents()

    outputProducts = Backend_Helper.refineResult(allDocs)
    return jsonify(outputProducts) #original from alfred


if __name__ == "__main__":
    app.run(port=5001, debug=True)
