
import csv
import sys


class tickerSymbol:
    def __init__(self, currentTimeStamp, symbolName, tradeQuantity, tradePrice ):
        self.symbolName = symbolName
        self.currentTimeStamp = currentTimeStamp
        self.tradeQuantity = tradeQuantity
        self.tradePrice = tradePrice
        self.maxPrice = 0
        self.sumOfProducts = 0
        self.sumOfWeights = 0
        self.weightedAvgPrice = 0
        self.maxTimeGap = 0
        self.tradeVolume = 0
        self.previousTimeStamp = 0

    def __eq__(self, otherTickerSymbol): 
        return self.symbolName == otherTickerSymbol.symbolName 

    def __iter__(self):
        return iter([self.symbolName, self.maxTimeGap, self.tradeVolume, self.weightedAvgPrice , self.maxPrice])

    def __repr__(self):
        return str(self)

    def getMaxTimeGap(self):
        return self.maxTimeGap

    def getTradeVolume(self):
        return self.tradeVolume

    def getWeightedAveragePrice(self):
        return self.weightedAvgPrice 

    def getMaxPrice(self):
        return self.maxPrice
    
    def getSymbolName(self):
        return self.symbolName
     
    def getTimeStamp(self):
        return self.currentTimeStamp

    def getMaxTimeGap(self):
        return self.maxTimeGap

    def getTradeQty(self):
        return self.tradeQuantity

    def getTradePrice(self):
        return self.tradePrice   

    def calculateWeightedAverage(self):
        self.weightedAvgPrice = int(self.sumOfProducts / self.sumOfWeights)
   
    #  Pseudocode for weighted average price: (self.tradeQuantity0 * self.tradePrice0)+ (self.tradeQuantity1 * self.tradePrice1) + ...(self.tradeQuantityi * self.tradePricei) / (sum of weights)
    def calculateWeightedAvgNumeratorDenominator(self):
        self.sumOfProducts += self.tradeQuantity * self.tradePrice
        self.sumOfWeights += self.tradeQuantity     
    
    # (if current max price < price read -> assign price read to max price variable); 
    def calculateMaxPrice(self):
        if(self.tradePrice > self.maxPrice) :
            self.maxPrice = self.tradePrice

    def calculateMaxTimeGap(self):
         #Check to see that this is the first time stamp 
        if (self.maxTimeGap == 0 and self.previousTimeStamp == 0):
            self.previousTimeStamp = self.currentTimeStamp
            #Replace maxtimegap with a bigger time gap
        elif (self.maxTimeGap < (self.currentTimeStamp - self.previousTimeStamp)) :
            self.maxTimeGap = self.currentTimeStamp - self.previousTimeStamp    
            self.previousTimeStamp = self.currentTimeStamp
            
    def accumulateTradeVolume(self):
        self.tradeVolume += self.tradeQuantity

   
    def mergeTwoDuplicates(self, secondObject):
        # IMPORTANT: Make Sure initial time step is performed before calling this function! 
        # Replace following attributes of hopefully oldest timestamped ticker. 
        self.currentTimeStamp = secondObject.getTimeStamp()
        self.tradeQuantity = secondObject.getTradeQty()
        self.tradePrice = secondObject.getTradePrice()

    def updateTradeSingleTimeStep(self):
        self.accumulateTradeVolume()
        self.calculateMaxTimeGap()
        self.calculateMaxPrice()
        self.calculateWeightedAvgNumeratorDenominator()

if len(sys.argv) > 1:

    #Read via stdin 
    reader = csv.reader(sys.stdin)
    csvInputName = sys.argv[1]
    csvOutputName = sys.argv[2]
    #count the number of rows in csv and use it to define the list of objects
    dataList = []
     #CREATE OBJECT PER SYMBOL PER LINE READ FROM CSV FILE. 
    with open(csvInputName, 'r', newline='') as f:
        reader = csv.reader(f)
        
        for row in reader:
            dataList.append(tickerSymbol(int(row[0]),row[1], int(row[2]), float(row[3]) ))   
           
                #TODO Optimize search extraction of item in question. 

 # Sort the list by alphabetical order and time Stamp Order   
    dataList.sort(key=lambda num: (num.getSymbolName(), num.getTimeStamp()))

    h = 0
   
    while h < len(dataList):
        j = h + 1
        #Initial Time step
        dataList[h].updateTradeSingleTimeStep()
        #Test for duplicate instances and update accordingly
        
        while j < len(dataList):
            if(dataList[h].getSymbolName() == dataList[j].getSymbolName()):
                dataList[h].mergeTwoDuplicates(dataList[j])
                dataList[h].updateTradeSingleTimeStep()
                del dataList[j]

            else:
                j += 1
        h += 1
    
    #Process the list 
    #CalculateWeightedAverage utilizing accumulated sum of products /sum of weights prior to printing output  
    # update Trade Single Time Step : ACCUMULATE NUMBER OF TRADES = VOLUME
    # KEEP ONLY MAX PRICE PREVIOUSLY READ
    x = 0
    while x < len(dataList):
        dataList[x].calculateWeightedAverage()
        x += 1
    
    #CSV WRITER PORTION (OUTPUT)
    with open(csvOutputName, 'w', newline='') as f:
        writer = csv.writer(f)
        for tSym in dataList :
            convertList = list(tSym)
            writer.writerow(convertList)
          


 

else:
  print("Either the csv doesn't exist or there is a problem with the syntax, try again!")
  exit(1)