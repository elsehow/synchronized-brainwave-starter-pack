from lib.featurevectorgenerator import feature_vector_generator
from dateutil.parser import parse
import numpy as np

# returns a list of dictionaries
# {subject_num: num_feature_vectors}
# (number of feature vectors between t0 and t1)
def num_feature_vectors(subjects, t0, t1):
  def genlength(gen):
    return len([n for n in gen])
  return [{subject: genlength(feature_vector_generator(subject, t0, t1))}
     for subject in subjects]

# time ranges for the math exercise in round 1
round1_math_t0 = parse('2015-05-09 23:33:28.876+00')
round1_math_t1 = parse('2015-05-09 23:33:58.875+00')

# see how many feature vectors we get from each round 1 subject in this range
# if each feature vector represents 3 seconds of data, we should see ~ 10 per subject
print num_feature_vectors(
  range(1,16),
  round1_math_t0,
  round1_math_t1)

# now let's do the same for round 2 subjects
# times for the round 2 math exercise
round2_math_t0 = parse('2015-05-09 23:44:26.341+00')
round2_math_t1 = parse('2015-05-09 23:44:56.343+00')
# find all feature vectors in this range for round 2 subjects
print num_feature_vectors(
  range(16,31),
  round2_math_t0,
  round2_math_t1)


# if you see fewer feature vectors than you'd expect, here are the possibilities:
# - some of the readings had a signal quality below the threshold -
# FIX: you can set the sq parameter in feature_vector_generator - e.g., sq=255 to keep all readings regardless of quality.
# - we oversampled in the time range
# FIX: get feature vectors from a slightly wider time range
# - no readings exist in that time
# FIX: well, no fix for this, but you can go into the source data files and check.
