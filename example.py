from lib.featurevectorgenerator import feature_vector_generator
from dateutil.parser import parse
from sklearn import svm
from sklearn import cross_validation
import numpy as np

def vectorsAndLabels(arrayOfGenerators):
  '''Takes an array of generators and produces two lists X and y
  where len(X) = len(y),
  X is the vectors, y is their (numerical) labels.'''
  X = []
  y = []
  currentLabel = 0
  for generator in arrayOfGenerators:
  	for vector in generator:
  		# NB: feature vectors are serialized as strings sometimes
  		# we map them to floats
  		X.append(vector)
  		y.append(currentLabel)
  	currentLabel+=1
  return X, y

def crossValidate(X,y):
  "7-fold cross-validation with an SVM with a set of labels and vectors"
  clf = svm.LinearSVC()
  scores = cross_validation.cross_val_score(clf, np.array(X), y, cv=7)
  return scores.mean()

# let's see how well we can distinguish between two subjects based on their brainwaves.
# we'll get their data from a specific time range:
t0 = parse('2015-05-09 23:28:00+00')
t1 = parse('2015-05-09 23:30:31+00')
# and make two generators of feature vectors for the two different subjects:
personA_gen = feature_vector_generator(9, t0, t1)
personB_gen = feature_vector_generator(13, t0, t1)
# now let's feed these feature vectors into an SVM
# and do 7-fold cross-validation.
X, y = vectorsAndLabels([personA_gen, personB_gen])
print crossValidate(X, y)
