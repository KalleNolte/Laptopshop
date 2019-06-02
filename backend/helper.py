class Backend_Helper:


    @staticmethod
    def clean_frontend_json(json_dict) :
        result = dict()
        for key in json_dict :
            result[key] = dict()
            for sub_key in json_dict[key] :
                if json_dict[key][sub_key] or Backend_Helper.is_integer(json_dict[key][sub_key]) or Backend_Helper.is_float(json_dict[key][sub_key]):
                    value = json_dict[key][sub_key]
                    if Backend_Helper.is_integer(value) :
                        value = int(value)
                    elif Backend_Helper.is_float(value) :
                        value = float(value)
                    result[key].update({sub_key:value})
                elif sub_key == "weight" and not json_dict[key][sub_key] :
                    result[key].update({sub_key:1})
        return result
    @staticmethod
    def refineResult(docs):
        outputProducts = []

        for hit in docs['hits']['hits']:
            item = {
              "asin": hit['_source']['asin'],
              "productTitle": hit['_source']['productTitle'],
              "price": hit['_source']['price'],
              "screenSize" : hit['_source']['screenSize'],
              "displayResolutionSize" : [hit['_source']['displayResolutionSize'][0], hit['_source']['displayResolutionSize'][1]],
              "processorSpeed" : hit['_source']['processorSpeed'],
              "processorType" : hit['_source']['processorType'],
              "processorCount" : hit['_source']['processorCount'],
              "processorManufacturer" : hit['_source']['processorManufacturer'],
              "ram" : hit['_source']['ram'],
              "brandName" : hit['_source']['brandName'],
              "hardDriveType" : hit['_source']['hardDriveType'],
              "ssdSize" : hit['_source']['ssdSize'],
              "hddSize": hit['_source']['hddSize'],
              "graphicsCoprocessor": hit['_source']['graphicsCoprocessor'],
              "chipsetBrand": hit['_source']['chipsetBrand'],
              "operatingSystem": hit['_source']['operatingSystem'],
              "itemWeight": hit['_source']['itemWeight'],
              #"memoryType": hit['_source']['memoryType'],
              "productDimension": [hit['_source']['productDimension'][0],hit['_source']['productDimension'][0],hit['_source']['productDimension'][0]],
              "color": hit['_source']['color'],
              "imagePath": hit['_source']['imagePath'],
              "avgRating": hit['_source']['avgRating'],

            }
            outputProducts.append(item)
        return outputProducts

    @staticmethod
    def is_integer(var) :
        try:
            int(var)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_float(var) :
        try:
            float(var)
            return True
        except ValueError:
            return False
