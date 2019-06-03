class ColorInformation:



  #data is the given json file trasmitted from angular
  #products should be initialized with ordered output set
  def __init__(self, data, products):
    self.data = data
    self.products = products
    self.matched = {}
    self.threshholdPrice = 0



  #extract searched key value pair
  #return as a dictionary---------
  #------------------------------#
  def extractKeyValuePairs(self):
    print(self.data)
    searchedValues = {}
    for key in self.data:
      #if type(self.data[key]) == type(dict()):
        for nestedKey in self.data[key]:
          if nestedKey != "weight" and self.data[key][nestedKey] != "":
            searchedValues[nestedKey] = self.data[key][nestedKey]
      #else:
        #print(key)
       # if self.data[key] != "" and key != 'weight':
        #  searchedValues[key]= self.data[key]
          #updated Version
          #searchedValues[key][key+"Value"]
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
    self.threshholdPrice = self.prozessThreshholdPrice(searchedValues)

    for laptop in self.products:

      # initial value for minValue, maxValue. May change later
      if 'minValue' in searchedValues:
        self.matched['price'] = 'green'
      if 'maxValue' in searchedValues:
        self.matched['price'] = 'green'


      for key in searchedValues:
      #special case for price field, containing 3 infos instead of 2-------------------------------------#
        if key   == 'minValue':
          self.prozessColorAttributePrice(searchedValues,laptop)
        elif key == 'maxValue':
          self.prozessColorAttributePrice(searchedValues,laptop)
      #--------------------------------------------------------------------------------------------------#

        else: #all other attributes
        # --------------------------------------------------------------------------------------------------#
        # Strings needs to be converted to lowercase-------------------------------------------------------#
          try:
            if ((laptop[key[:-5]] is not None)and not laptop[key[:-5]].lower() == searchedValues[key].lower()):
              self.matched[key[:-5]] = 'red'
            else:
              self.matched[key[:-5]] = 'green'
        #--------------------------------------------------------------------------------------------------#

        #Numbers cant be converted, so except for control flow if lower() - function fails-----------------#
          except:
            if ((laptop[key[:-5]] is not None) and not laptop[key[:-5]] == searchedValues[key]):
              self.matched[key[:-5]] = 'red'
            else:
             self.matched[key[:-5]] = 'green'
        #---------------------------------------------------------------------------------------------------#


      #Sort the created matched dict ----------------------------------------#
      matchedSortedKeys = sorted(self.matched.keys())
      matchedSorted = {}
      for key in matchedSortedKeys:
        matchedSorted[key] = self.matched[key]
      laptop["matched"] = matchedSorted
      self.matched = {}
      #----------------------------------------------------------------------#



  #Calculation of threshhold--------------------#
  #---------------------------------------------#
  def prozessThreshholdPrice(self,searchedValues):
    threshhold = 0
    if 'minValue' and 'maxValue' in searchedValues:
      threshhold = (float(searchedValues['maxValue']) - float(searchedValues['minValue']))
    elif 'minValue' in searchedValues:
      threshhold = float(searchedValues['minValue']) / 10
    elif 'maxValue' in searchedValues:
      threshhold = float(searchedValues['maxValue']) / 10
    print(threshhold)
    return threshhold




  #Price can be green, yellow or red, depending on the threshhold-----------------#
  #-------------------------------------------------------------------------------#
  def prozessColorAttributePrice(self,searchedValues,laptop):
    try:
      if (laptop["price"] >= float(searchedValues['minValue'])-self.threshholdPrice):
        if (float(laptop["price"]) < float(searchedValues["minValue"])):
          self.matched['price'] = 'yellow'
      else:
        self.matched['price'] = 'red'
    except:
      pass
    try:
      if (laptop["price"] <= float(searchedValues['maxValue'])+self.threshholdPrice):
        if (float(laptop["price"]) > float(searchedValues["maxValue"])):
          self.matched['price'] = 'yellow'
      else:
        self.matched['price'] = 'red'
    except:
      pass








