__author__ = 'Andrei Gurguta'


import backend   # the module where functions reside


# Generate the training and test data set. The source is split by the ratio passed in the second parameter:
ProcessedList = backend.generateDataSets("http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data",50)


# ProcessList holds both the Training set and the Test set.
TrainingDataSet = ProcessedList[0]
TestDataSet     = ProcessedList[1]


# Build (train) the classifier. Please see backend.py for details of internal structure of the
# classifier (basically a list of 2 dictionaries holding averages(or weights) for the 2 possible outcomes)
# Also backend.py holds a note why  I'm not using a midpoint classifier like in the cancer example (line 135):
TheClassifier = backend.trainClassifier(TrainingDataSet)

# Test the classifier:
# the function will return a list of the accuracy of the total prediction and a list of summary results for each row
# plese see backend.py for internal structure details:
Result = backend.testClassifierAccuracy(TestDataSet,TheClassifier)

print("The classifier's accuracy against the test data set was: {0:.2f}%".format(Result[0]))

# Check to see if user needs printing of summary results for testing each row in the Test data set"
ErrorFlag = False
while ErrorFlag == False:
    # some simple "error" raising
    Prnt = input("Would you like to print a summary of Testing the classifier against Data Set? (Y/N): ")
    if Prnt.lower() == "y":
        backend.printSummaryResults(Result[1])
        ErrorFlag = True
    elif Prnt.lower() == "n":
        ErrorFlag = True
    else:
        print("WARNING: I don't understand your answer, please type Y for Yes or N for No...")





