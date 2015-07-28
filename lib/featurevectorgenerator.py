from lib import querying
from lib import brainlib
from lib.grouper import grouper
from itertools import izip_longest
from dateutil.parser import parse
import numpy as np

# make a generator of feature vectors
# given a subject and a range of times
#
# example usage:
#
# subject_num = 11
# t0 = parse('2015-05-09 23:28:46+00')
# t1 = parse('2015-05-09 23:29:46+00')
# gen = feature_vector_generator(subject_num, t0,t1)


# utility functions

def parse_raw_values (reading):
  "make list of power spectra for all raw_values in a list"
  # first and last values have { and } attached.
  vals = reading['raw_values'].split(',')
  vals[0] = vals[0][1:]
  vals[len(vals)-1] = vals[len(vals)-1][:-1]
  return np.array(vals).astype(np.float)

# get the power spectrum
def spectra (readings):
  "Parse + calculate the power spectrum for every reading in a list"
  return [brainlib.pSpectrum(parse_raw_values(r)) for r in readings]


# configure feature vector generation here:

vector_resolution = 3 # number of readings in an averaged feature vector

def make_feature_vector (readings): # A function we apply to each group of power spectra
  '''
  Create 100, log10-spaced bins for each power spectrum.
  For more on how this particular implementation works, see:
  http://coolworld.me/pre-processing-EEG-consumer-devices/
  '''
  return brainlib.avgPowerSpectrum(
    brainlib.binnedPowerSpectra(spectra(readings), 100)
    , np.log10)


# feature vector generator

def feature_vector_generator (subject, t0, t1):
  '''Returns a generator of feature vectors
  based on the config variables above'''
  # get all the readings for subject between t0 and t1
  readings = querying.readings(subject, t0, t1)
  # group readings into lists of length `vector_resolution`
  groups = grouper(vector_resolution, readings)
  for g in groups:
    readings = filter(None, g)
    # throw out readings with fewer signals than our desired resolution
    if len(readings) == vector_resolution:
      yield make_feature_vector(readings)

