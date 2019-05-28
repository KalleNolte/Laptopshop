class WeightningSearchFunctions:

  #data is the given json file trasmitted from angular
  #products should be initialized with ordered output set
  def __init__(self, data, products):
    self.data = data
    self.products = products

  #extract searched key value pair
  #return as a dictionary
  def extractKeyValuePairs(self):
    print(self.data)
    searchedValues = {}
    for key in self.data:
      if type(self.data[key]) == type(dict()):
        for nestedKey in self.data[key]:
          if self.data[key][nestedKey] != "":
            searchedValues[nestedKey] = self.data[key][nestedKey]
      else:
        if self.data[key] != "":
          searchedValues[key] = self.data[key]
    return searchedValues

  #add for each laptop in products the matched key with nested key - value pairs
  #   Example:
  #   ...
  #   matched{
  #     'brandName': True,
  #     'price': False
  #     'hardDriveType': True
  #   }
  #
  def prozessDataBinary(self,searchedValues):
    matched = {}

    if "minValue" or "maxValue" in searchedValues:
      matched['price'] = 'green';

    for laptop in self.products:
      for key in searchedValues:
        if key == ("minValue"):
          if (laptop["price"] <= float(searchedValues[key])):
            matched['price'] = 'red'
        elif key == ("maxValue"):
          if (laptop["price"] >= float(searchedValues[key])):
            matched['price'] = 'red'
        elif ((laptop[key] is not None)and not laptop[key].lower() == searchedValues[key].lower()):
          matched[key] = 'red'
        else:
          matched[key] = 'green'

      #Sort the matched dict
      matchedSortedKeys = sorted(matched.keys())
      matchedSorted = {}
      for key in matchedSortedKeys:
        matchedSorted[key] = matched[key]
      laptop["matched"] = matchedSorted
      matched = {}


 def prozessDataPrice(self,searchedValues):
   threshhold = 







