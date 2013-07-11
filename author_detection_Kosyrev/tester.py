# -*- coding: utf-8 -*-

from sklearn.externals import joblib
from toolkit import getClassificationData

# import numpy as np

from toolkit import readMessagesFromFile, trimMessageList, Vectorizer
from os import listdir
from os.path import isfile, join

import warnings
warnings.simplefilter("ignore", DeprecationWarning)

def main():
  dbPath = './test_db/'
  vectSize = 780
  msgLen = 440
  
  gen = Vectorizer('./params/globaldict.txt', vectSize)
  classMap = gen.getClassMap()
  
#   print 'Loading classifier...  ',
  classifier = joblib.load('./classifiers/clf_01.pkl')
#   print 'Done!'

  
  # Print score per author 
  fileList = [ f for f in listdir(dbPath) if isfile(join(dbPath,f)) ]
  for userName in fileList:
    messageList = trimMessageList( readMessagesFromFile( join(dbPath, userName) ), msgLen )
    i = 0
    for message in messageList:
      vect = gen.getVect(message)
      if classMap[int(classifier.predict(vect))] in userName: i+=1
    print '%s: %s' %( userName[:-4], round(float(i)/float(len(messageList)), 2) )

  
  sampleVectors, classes = getClassificationData(dbPath, vectSize, msgLen)
  
#   sampleVectors = np.array(sampleVectors)
#   classes = np.array(classes)
  
  print 'Total score: %s' %str(round(classifier.score(sampleVectors, classes), 2))
  
if __name__ == '__main__':
  main()