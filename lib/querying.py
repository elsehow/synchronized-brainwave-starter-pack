import csv
import os.path as path
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

# Utilities to query date ranges from the indra dataset
#
# EXAMPLE USAGE
#
# subject_num = 11
# t0 = parse('2015-05-09 23:28:46+00')
# t1 = parse('2015-05-09 23:29:46+00')
# readings(subject_num, t0, t1)

class DatasetQueryError (Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

def dataset_path (subjectnum):
  return path.join('dataset', 'neurosky-data', str(subjectnum) + '.csv')

def synced_time (row):
  '''Gets indra time.
  You can change the field to get, for example,
  'readingTime' or 'createdAt'.'''
  return parse(row['indra_time'])

def readings_in_range (csvdict, t0, t1):
  '''A generator that returns all readings in a CSV dict
  not including t0, including t1. You can only use this generator
  if the file is open for reading.'''
  inrange = False
  for row in csvdict:
    time = synced_time(row)
    if not inrange and time >= t0:
      inrange = True
    if inrange:
      yield row
    if inrange and time >= t1:
      break

def readings (subject, t0, t1):
  '''Returns all of subject's readings between t0 and t1,
  not including t0, but including t1'''
  if t1 < t0:
    raise DatasetQueryError("First time must come before second time.")
  with open(dataset_path(subject), 'r') as f:
    reader = csv.DictReader(f)
    return [r for r in readings_in_range(reader, t0, t1)]
