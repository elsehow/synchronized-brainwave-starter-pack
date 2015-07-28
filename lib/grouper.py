from itertools import izip_longest

def grouper(n, iterable, fillvalue=None):
  "grouper('ABCDEFG', 3, 'x') --> 'ABC' 'DEF' 'Gxx'"
  args = [iter(iterable)] * n
  return izip_longest(*args, fillvalue=fillvalue)
