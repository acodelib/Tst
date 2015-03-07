__author__ = 'Andrei'

import functions

ProcessedList = functions.generateDataSets("http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data",50)
#the second param above is used to determine the ration of spliting the data in a set for training and one for test

TrainingDataSet = ProcessedList[0]
TestDataSet     = ProcessedList[1]

TheClassifier = functions.trainClassifier(TrainingDataSet)

Result = functions.testClassifierAccuracy(TestDataSet,TheClassifier)

print("The classifier's accuracy against the test data set was: {0:.2f}%".format(Result[0]))




# functions.generateClassifier(TrainingDataSet)

