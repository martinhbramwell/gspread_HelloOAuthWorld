#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json

def dict2obj(aDict):
    top = type('new', (object,), aDict)
    seqs = tuple, list, set, frozenset
    for i, j in aDict.items():
    	if isinstance(j, dict):
    	    setattr(top, i, dict2obj(j))
    	elif isinstance(j, seqs):
    	    setattr(top, i, 
    		    type(j)(dict2obj(sj) if isinstance(sj, dict) else sj for sj in j))
    	else:
    	    setattr(top, i, j)
    return top

def put(data, filename):
  jsondata = json.dumps(data, indent=4, skipkeys=True, sort_keys=True)
  print 'A'
  try:
    print 'B'
    jsondata = json.dumps(data, indent=4, skipkeys=True, sort_keys=True)
    print 'C'
    fd = open(filename, 'w')
    print 'D'
    fd.write(jsondata)
    print 'E'
    fd.close()
    print 'F'
  except:
    print 'ERROR writing', filename
    pass

def get(filename):
  aDict = {}
  try:
    fd = open(filename, 'r')
    text = fd.read()
    fd.close()
    aDict = json.loads(text)
  except: 
    print 'COULD NOT LOAD:', filename

  return aDict

def getObj(filename):
  return dict2obj(get(filename))
  


if __name__ == '__main__':

  o = get(sys.argv[1]);
  if o:
    print "Got : %s" % (dict2obj(o).installed.client_secret)
    put(o, "new_" + sys.argv[1]);
    # print "Done."
  else:
    print "Huh? %s" % (sys.argv[1])

  
