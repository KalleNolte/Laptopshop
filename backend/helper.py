class Backend_Helper:


    @staticmethod
    def clean_frontend_json(json_dict) :
        result = dict()
        for field in json_dict :
            field_value_name = field+"Value"
            field_range_name = field+"Range"
            if field_range_name in json_dict[field] :
                if len(json_dict[field][field_range_name]) > 0 :
                    result.update({field:json_dict[field]})
            elif field_value_name in json_dict[field] :
                if len(json_dict[field][field_value_name]) > 0 :
                    result.update({field:json_dict[field]})
        # print("after cleanfin",result)

        return result
    @staticmethod
    def clean_for_alexa(json_dict):
        #data[intent_variable].update({"intent":intent,"value":intent_variable_value})
        result = dict()
        intent = json_dict["intent"]
        intent_variable = json_dict["intentVariable"]
        intent_variable_value = json_dict[json_dict["intentVariable"]][json_dict["intentVariable"]+"Value"]
        for field_name in json_dict:
            field_value_name = field_name+"Value"
            if field_name == "intentVariable" or field_name == "intent":
                pass
            elif field_value_name in  json_dict[field_name] :
                if Backend_Helper.is_integer(json_dict[field_name][field_value_name]):
                    value = int(json_dict[field_name][field_value_name])
                elif Backend_Helper.is_float(json_dict[field_name][field_value_name]):
                    value = float(json_dict[field_name][field_value_name])
                else :
                    value = json_dict[field_name][field_value_name]

                result.update({field_name:{field_value_name : [value],"weight":4}})
        result.update({json_dict["intentVariable"]:{"intent":intent,"value":intent_variable_value}})
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
