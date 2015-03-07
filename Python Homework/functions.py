__author__ = 'Andrei'

import httplib2

# Defining immutables to use in dictionaries keys (will be defining each row from a source data set as a dictionary)
AGE        = "Age"
WCLASS     = "Workclass"
EDUCATION  = "Education"
MARSTATUS  = "Marital-Status"
OCCUPATION = "Occupation"
RELANTION  = "Relationtip"
RACE       = "Race"
SEX        = "Sex"
CAPGAIN    = "Capital-gain"
CAPLOSS    = "Capital-loss"
HPW        = "Hours per week"
RESULT     = "Result either <=50K or >50k"

#***************************************************************************************************
def generateDataSets(WebLinkToData,TrnSizePrcnt):
    '''
    takes in link to a web data repository readable by hhttplib2 and generates two lists,
    the Training and Test sets
    :param WebLinkToData: web address
           TrainingSize:  percentage ratio of data to make up the training set size
    :return: a list holding two other list
    '''
    RowNumbers         = 0
    TrainingListSize   = 0
    LineCnt            = 0
    ReturnList         = []
    Training           = []
    Test               = []


    #load data from online source:
    InternalHandle = httplib2.Http(".cache")
    Resp , Content = InternalHandle.request(WebLinkToData,"GET")
    StrData        = Content.decode('UTF-8')

    # set size of the training data set and load separate rows into a list
    RowNumbers       = StrData.count("\n")
    TrainingListSize = int( RowNumbers * (TrnSizePrcnt/100))
    PlaceHold        = StrData.split("\n")
    # Note to ask teacher: removing last 2 empty items in the list resulted from the above split - not sure why this occurs, have observed it while debugging
    PlaceHold.pop()
    PlaceHold.pop()

    # further split of data into dictionaries of data for each subject (Row)
    # code will generate both Training and Test dicts according to ratio passed to function
    print("...Loading data...")
    for items in PlaceHold:
        TempList   = items.split(",")
        Line = {}
        Line[AGE]           = int(TempList[0])
        Line[WCLASS]        = TempList[1].strip()
        Line[EDUCATION]     = int(TempList[4])
        Line[MARSTATUS]     = TempList[5].strip()
        Line[OCCUPATION]    = TempList[6].strip()
        Line[RELANTION]     = TempList[7].strip()
        Line[RACE]          = TempList[8].strip()
        Line[SEX]          = TempList[9].strip()
        Line[CAPGAIN]       = int(TempList[10])
        Line[CAPLOSS]       = int(TempList[11])
        Line[HPW]           = int(TempList[12])
        Line[RESULT]        = TempList[14].strip()
        LineCnt     = LineCnt + 1
        if LineCnt <= TrainingListSize:
            Training.append(Line)
        else:
            Test.append(Line)
    print ("-> successufully loaded {} rows".format(RowNumbers))
    print

    ReturnList.append(Training)
    ReturnList.append(Test)

    print("-> Training set comprises of {0} rows \n-> Test set comprises of {1} rows".format(TrainingListSize,(RowNumbers-TrainingListSize)))

    return ReturnList
#***************************************************************************************************
def trainClassifier(TestList):
    PositiveAge_Count = 0
    NegativeAge_Count = 0
    TheClassifier = []
    Positive = {}       # These two dictionaries will be used to hold sums/occurences for the two possible outvomes
    Negative = {}

    # Prepare members of the dictionary:
    Positive[AGE]           = 0
    Positive[WCLASS]        = {}
    Positive[EDUCATION]     = 0
    Positive[MARSTATUS]     = {}
    Positive[OCCUPATION]    = {}
    Positive[RELANTION]     = {}
    Positive[RACE]          = {}
    Positive[SEX]          = {}
    Positive[CAPGAIN]       = 0
    Positive[CAPLOSS]       = 0
    Positive[HPW]           = 0
    Positive[RESULT]        = '>50'

    Negative[AGE]           = 0
    Negative[WCLASS]        = {}
    Negative[EDUCATION]     = 0
    Negative[MARSTATUS]     = {}
    Negative[OCCUPATION]    = {}
    Negative[RELANTION]     = {}
    Negative[RACE]          = {}
    Negative[SEX]          = {}
    Negative[CAPGAIN]       = 0
    Negative[CAPLOSS]       = 0
    Negative[HPW]           = 0
    Negative[RESULT]        = '<=50'

    # This loop will generate the 2 sum lists for the <=50k or >50K
    for Elems in TestList:
        if Elems[RESULT] == ">50K":
            # Add/Operate the attributes of this row to the Positive List.
            # Means it will sum numeric attributes and count occurences for the string discrete ones
            Positive = sumDictionary(Positive,Elems)
            PositiveAge_Count += 1
        else:
            # Add/Operate the attributes of this row to the Negatives List.
            Negative = sumDictionary(Negative,Elems)
            NegativeAge_Count += 1

    #Now the two dictionaries above will be averaged (or weighted for discrete string attributes):
    averageTheDictionary(Positive,PositiveAge_Count)
    averageTheDictionary(Negative,NegativeAge_Count)

    # I have chosen to have the classifier comprised of both the Positive and Negative - I believe it's easier to compare with Test Values?
    TheClassifier.append(Positive)
    TheClassifier.append(Negative)

    return  TheClassifier
#***************************************************************************************************
def operateOnDiscrete(SomeDictionary,TestKey):
    '''
    Used in "summing" the discrete values
    Basically it counts the number of occurences per key to be wheighted out of the total.
    If key doesn't exist it will be added to the Dict
    '''
    if TestKey in SomeDictionary:
        SomeDictionary[TestKey]= SomeDictionary[TestKey] + 1
    else:
        SomeDictionary[TestKey]=1
#***************************************************************************************************
def operateWeight(SomeDictionary):
    '''
    The weght part for the Discrete values
    Basically for each attribute: counts occurences of each value then weights it out of the total for the attribute
    '''
    Sum = 0
    for Key,Elem in SomeDictionary.items():
        Sum = Sum + Elem
    for Key,Elem in SomeDictionary.items():
        SomeDictionary[Key]=Elem/Sum
    return SomeDictionary
#***************************************************************************************************
def sumDictionary(TheDictionary,NewValues):
    '''
    This does the summing part.
    Fof the discrete attributes it will perform the operateOnDiscrete function, for example for the WCLASS attribute
    '''
    TheDictionary[AGE]           = TheDictionary[AGE] +NewValues[AGE]
    operateOnDiscrete(TheDictionary[WCLASS],NewValues[WCLASS])
    TheDictionary[EDUCATION]     = TheDictionary[EDUCATION] + NewValues[EDUCATION]
    operateOnDiscrete(TheDictionary[MARSTATUS],NewValues[MARSTATUS])
    operateOnDiscrete(TheDictionary[OCCUPATION],NewValues[OCCUPATION])
    operateOnDiscrete(TheDictionary[RELANTION],NewValues[RELANTION])
    operateOnDiscrete(TheDictionary[RACE],NewValues[RACE])
    operateOnDiscrete(TheDictionary[SEX],NewValues[SEX])
    TheDictionary[CAPGAIN]       = TheDictionary[CAPGAIN] + NewValues[CAPGAIN]
    TheDictionary[CAPLOSS]       = TheDictionary[CAPLOSS] + NewValues[CAPLOSS]
    TheDictionary[HPW]           = TheDictionary[HPW] + NewValues[HPW]

    return TheDictionary
#***************************************************************************************************
def averageTheDictionary(TheDictionary,Count):
    '''
    TheDictionary holding the sums will be 'averaged'.
    This means that the numeric attributes will be averaged while the Discrete ones will be weighted.
    '''
    TheDictionary[AGE]        = TheDictionary[AGE] /Count
    TheDictionary[WCLASS]     = operateWeight(TheDictionary[WCLASS])
    TheDictionary[EDUCATION]  = TheDictionary[EDUCATION] /Count
    TheDictionary[MARSTATUS]  = operateWeight(TheDictionary[MARSTATUS])
    TheDictionary[OCCUPATION] = operateWeight(TheDictionary[OCCUPATION])
    TheDictionary[RELANTION]  = operateWeight(TheDictionary[RELANTION])
    TheDictionary[RACE]       = operateWeight(TheDictionary[RACE])
    TheDictionary[SEX]       = operateWeight(TheDictionary[SEX])
    TheDictionary[CAPGAIN]    = TheDictionary[CAPGAIN]/Count
    TheDictionary[CAPLOSS]    = TheDictionary[CAPLOSS]/Count
    TheDictionary[HPW]        = TheDictionary[HPW]/Count
#***************************************************************************************************
def testClassifierAccuracy(TestDataSet,Classifier):
    '''
    Tests each row(dictionary in the data set against the Classifier.
    '''
    print ("...Using Classifier to predict outcomes for the Test Data Set")
    RowCounter = 0
    SummaryResultList = []          # List to hold the actual result, the predicted result and a count of successful predictions
    RowsAccuracy = 0
    AccuracyPerc = 0
    ReturnResults = []

    for Rows in TestDataSet:
        RowCounter += 1
        RowResults = predictOutcome(Rows,Classifier)        # will look at all values in the dictionary and compare it with the Classifier. Will retun a list of predictions per each attribute
        RowPrediction = checkRowPrediction(RowResults)      #Based on the prediction above for each attribute it will predict for the whole Row
        LineResultList = []                                 # Loead the results per row into a temporary list
        LineResultList.append(RowCounter)
        LineResultList.append(RowPrediction)
        LineResultList.append(RowResults[11])
        if RowPrediction == RowResults[11]:                 # this is where accuracy is tested and counted
            LineResultList.append(1)
        else:
            LineResultList.append(0)
        SummaryResultList.append(LineResultList)            # add the temp list to a summary of all lines in the test data set
    print("-> Successfully tested {} rows for the Test Data Set".format(RowCounter))
    print("...Checking prediction accuracy...")
    for AccuracyCount in SummaryResultList:
        RowsAccuracy = RowsAccuracy + AccuracyCount[3]      #looks at over all accuracy

    AccuracyPerc = (RowsAccuracy / RowCounter)*100          #produces the accuracy performance result
    ReturnResults.append(AccuracyPerc)
    ReturnResults.append(SummaryResultList)

    return ReturnResults
#***************************************************************************************************
def predictOutcome(Row,Classifier):
    '''
    Works on an individual Row in the data set
    it checks for each row and
        if Numeric Attribute then
            operateNumericAttribute: looks at which is closer to the value, either the Positive or the Negative and produces a result based on that
        if dicrete Attribute then
            check the weight (or existence) of the Attribute in the Positive or Negative and produces a result based on that
    '''
    DiffPositive = 0
    DiffNegative = 0

    Positives = Classifier[0]
    Negatives = Classifier[1]

    RowStatus = []
    RowStatus.append(operateNumericAttribute(Positives[AGE],Negatives[AGE],Row[AGE]))
    RowStatus.append(operateDiscreteAttribute(Positives[WCLASS],Negatives[WCLASS],Row[WCLASS]))
    RowStatus.append(operateNumericAttribute(Positives[EDUCATION],Negatives[EDUCATION],Row[EDUCATION]))
    RowStatus.append(operateDiscreteAttribute(Positives[MARSTATUS],Negatives[MARSTATUS],Row[MARSTATUS]))
    RowStatus.append(operateDiscreteAttribute(Positives[OCCUPATION],Negatives[OCCUPATION],Row[OCCUPATION]))
    RowStatus.append(operateDiscreteAttribute(Positives[RELANTION],Negatives[RELANTION],Row[RELANTION]))
    RowStatus.append(operateDiscreteAttribute(Positives[RACE],Negatives[RACE],Row[RACE]))
    RowStatus.append(operateDiscreteAttribute(Positives[SEX],Negatives[SEX],Row[SEX]))
    RowStatus.append(operateNumericAttribute(Positives[CAPGAIN],Negatives[CAPGAIN],Row[CAPGAIN]))
    RowStatus.append(operateNumericAttribute(Positives[CAPLOSS],Negatives[CAPLOSS],Row[CAPLOSS]))
    RowStatus.append(operateNumericAttribute(Positives[HPW],Negatives[HPW],Row[HPW]))
    RowStatus.append(Row[RESULT])

    return  RowStatus
#***************************************************************************************************
def operateNumericAttribute(TestPositive,TestNegative,RowValue):
    '''
    Basicaly looks at which Average(either the Positive or the Negative) is closer to the actual value and
    returns a prediction based on that
    '''
    DiffPositive = abs(TestPositive - RowValue)
    DiffNegative = abs(TestNegative - RowValue)

    if DiffPositive <= DiffNegative:
        return ">50K"
    else:
        return  "<=50K"
#***************************************************************************************************
def operateDiscreteAttribute(TestPositive,TestNegative,RowValue):
    '''
    Checks first : if the Discrete is missing from either Positive or Negative and returns a prediction.(ex: if the Values doesn't exist in the Positives then it is a Negative)
    If the Discrete val is in both of them it looks at the weights and predicts based on that
    '''
    if RowValue not in TestPositive.keys():         # this is how it checks the existance of the key (the Attribute value) in the Positives and Negatives
        return  "<=50K"
    elif RowValue not in TestNegative.keys():
        return ">50K"
    elif TestPositive[RowValue] >= TestNegative[RowValue]:
        return ">50K"
    else:
        return  "<=50K"
#***************************************************************************************************
def checkRowPrediction(PredictedList):
    '''
    It will sum up the prediction for an entire row.
    Ex: If most of the attributes are Positive then it returns Positive prediction and so on
    '''
    ActualResult            = PredictedList[11]
    CorrectAttributeResults = 0
    RowResult               = ""


    for Index in range(10):
        if PredictedList[Index] == ActualResult:
            CorrectAttributeResults += 1

    if CorrectAttributeResults > 5:
        RowResult = ActualResult
    elif ActualResult == ">50K":
        RowResult = "<=50K"
    else:
        RowResult = ">50K"

    return RowResult
#***************************************************************************************************
