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
        print("after cleanfin",result)

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
