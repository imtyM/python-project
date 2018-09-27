from Classes.serialClass import serialClass
from Classes.mongoDB import mongoDB
from Classes.algorithms import algorithms
import pandas
import itertools
import numpy

PRIMARY_STRING = "primary_print."


# dataframe = pandas.read_csv("input_training_data.csv", header=None)
# dataset = dataframe.values
# X = dataset[:,:].astype(float)

# dataframe = pandas.read_csv("output_training_data.csv", header=None)
# dataset = dataframe.values
# Y = dataset
# Y = list(itertools.chain.from_iterable(Y))
# Y = numpy.array(Y)
    
myDB = mongoDB('field_collection_11092018')
processor = algorithms(myDB)

inputData_A4 = {
    "e77f": 60.5,
    "f566": 44.25,
    "f565": 46.75,
    "e77e": 45,
    "f57a": 46,
    "f567": 40
}
inputData_A3 = {
    "e77f": 66.5,
    "f565": 39.75,
    "e77e": 47,
    "f567": 39
}
inputData_D4 = {
    "e77f": 68.5,
    "f566": 46.75,
    "e77e": 51.25,
    "f57a": 45.0,
    "f565": 48.5
}


inputData_D4 = {
    "e77f": 71.5,
    "f566": 40.75,
    "e77e": 49.25,
    "f57a": 49.0,
    "f565": 45.5
}

inputData_C2 = {

    "e77f": 77.5,
    "f566": 48.75,
    "e77e": 53.25,
    "f57a": 52.875,
    "f565": 51.5
}



inputData_A1 = {

    "e77f": 70.0,
    "e77e": 46.75,
    "f565": 39.875,
    "f567": 35.0,
    "f57a": 44.625,

}

G2 = {
    "e77f": 78.0,
    "e77e": 53.0,
    "f57a": 51.22,
    "f565": 46.0,
    "f566": 44.33
}

G3 = {
    "f57a": 50.67,
    "f565": 45.11,
    "e77f": 63,
    "e77e": 45.67,
    "f567": 36.0
}

G9_1 = {
    "e77f": 84,
    "e77e": 63,
    "f57a": 46,
    "f565": 37
}

processor.debugProcess(G9_1)

# for i,data in enumerate(X):
#     inputData = {
#         "e77e": data[0],
#         "e77f": data[1],
#         "f565": data[2],
#         "f567": data[3]
#     }
#     processor.debugProcess(inputData)
#     print('Sample location is : ', Y[i])