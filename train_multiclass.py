import numpy
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
import itertools

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)
numpy.set_printoptions(threshold=numpy.inf)

# load dataset
dataframe = pandas.read_csv("input_training_data.csv", header=None)
dataset = dataframe.values
X = dataset[:,:].astype(float)
print(X)

dataframe = pandas.read_csv("output_training_data.csv", header=None)
dataset = dataframe.values
Y = dataset
Y = list(itertools.chain.from_iterable(Y))
Y = numpy.array(Y)
print(Y)



# encode class values as integers
encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)
print(dummy_y)

# define baseline model
def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(8, input_dim=4, activation='relu'))
	model.add(Dense(16, activation='relu'))
	model.add(Dense(16, activation='relu'))
	model.add(Dense(16, activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

print("creating estimator")
estimator = KerasClassifier(build_fn=baseline_model, epochs=400, batch_size=5, verbose=1)

print("creating kfold")
kfold = KFold(n_splits=10, shuffle=True, random_state=seed)

# execute model
print('executing model')
results = cross_val_score(estimator, X, dummy_y, cv=kfold)
print("Baseline: %.3f%% (%.2f%%)" % (results.mean()*100, results.std()*100))