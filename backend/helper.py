class Backend_Helper:


    @staticmethod
    def clean_frontend_json(json_dict) :
        result = dict()
        for key in json_dict :
            result[key] = dict()
            for sub_key in json_dict[key] :
                if json_dict[key][sub_key] or type(json_dict[key][sub_key]) is list or Backend_Helper.is_integer(json_dict[key][sub_key]) or Backend_Helper.is_float(json_dict[key][sub_key]):
                    value = json_dict[key][sub_key]
                    if type(json_dict[key][sub_key]) is not list and Backend_Helper.is_integer(value) :
                        value = int(value)
                    elif type(json_dict[key][sub_key]) is not list and Backend_Helper.is_float(value) :
                        value = float(value)
                    result[key].update({sub_key:value})
                elif sub_key == "weight" and not json_dict[key][sub_key] :
                    result[key].update({sub_key:1})
        return result

    @staticmethod
    def refineResult(docs):
        outputProducts = []

        for hit in docs['hits']['hits']:

            item = dict()

            for field in hit["_source"]:
                item.update({field:hit["_source"][field]})

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
