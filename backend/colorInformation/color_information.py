class ColorInformation:

  #data is the given json file trasmitted from angular
  #products should be initialized with ordered output set
  def __init__(self, data, products):
    self.data = data
    self.products = products
    self.matched = {}

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
  #     'brandName': 'green',
  #     'price': 'red',
  #     'hardDriveType': 'green'
  #   }
  #
  def prozessDataBinary(self,searchedValues):
    print(searchedValues)
    #matched = {}

    for laptop in self.products:

      if "minValue" or "maxValue" in searchedValues:
        self.matched['price'] = 'green';

      for key in searchedValues:
        if key == 'minValue':
          self.prozessColorAttributePrice(searchedValues,laptop)
        elif key == 'maxValue':
          self.prozessColorAttributePrice(searchedValues,laptop)
        elif ((laptop[key] is not None)and not laptop[key].lower() == searchedValues[key].lower()):
          self.matched[key] = 'red'
        else:
          self.matched[key] = 'green'

      #Sort the matched dict
      matchedSortedKeys = sorted(self.matched.keys())
      matchedSorted = {}
      for key in matchedSortedKeys:
        matchedSorted[key] = self.matched[key]
      #print(matchedSorted)
      #print(self.matched)
      laptop["matched"] = matchedSorted
      self.matched = {}



  def prozessThreshholdPrice(self,searchedValues):
    threshhold = 0
    if 'minValue' and 'maxValue' in searchedValues:
      threshhold = (float(searchedValues['maxValue']) - float(searchedValues['minValue']))
    elif 'minValue' in searchedValues:
      threshhold = float(searchedValues['minValue']) / 10
    elif 'maxValue' in searchedValues:
      threshhold = float(searchedValues['maxValue']) / 10
    return threshhold


  def prozessColorAttributePrice(self,searchedValues,laptop):
    try:
      if (laptop["price"] >= float(searchedValues['minValue'])-self.prozessThreshholdPrice(searchedValues)):
        if (float(laptop["price"]) < float(searchedValues["minValue"])):
          self.matched['price'] = 'yellow'
      else:
        self.matched['price'] = 'red'
    except:
      1+1
    try:
      if (laptop["price"] <= float(searchedValues['maxValue'])+self.prozessThreshholdPrice(searchedValues)):
        if (float(laptop["price"]) > float(searchedValues["maxValue"])):
          self.matched['price'] = 'yellow'
      else:
        self.matched['price'] = 'red'
    except:
      1+1








