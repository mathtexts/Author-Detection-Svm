# -*- coding: utf-8 -*-

import sys
from sklearn import svm
from sklearn.externals import joblib
from toolkit import getClassificationData

# import numpy as np
# from sklearn import linear_model


def main():
  
  noOutput = False
  
  args = sys.argv[1:]
  if not args:
    vectorSize = 780
    msgLen = 440
    fC = float(0.2)
  else:
    vectorSize = int(args[0])  
    msgLen = int(args[1])  
    fC = float(args[2])  
    noOutput = True
    
  if not noOutput: print 'Loading train data...  ',
  trainList, classes = getClassificationData('./db/', vectorSize, msgLen)
  sampleVectors, testClasses = getClassificationData('./test_db/', vectorSize, msgLen)
  if not noOutput: print 'Done!'

#   trainList = np.array(trainList)
#   classes = np.array(classes)
  
  
  classifier = svm.LinearSVC(class_weight = 'auto', C=fC)
  classifier.fit(trainList, classes)  
  print  'Score: %s' %round(classifier.score(sampleVectors, testClasses), 2)
#    
#   classifier = linear_model.SGDClassifier(class_weight = 'auto', fit_intercept=False, n_iter=100, shuffle=True, n_jobs=2)
#   classifier.fit(trainList, classes)  
#   print  'Score: %s' %round(classifier.score(sampleVectors, testClasses), 2)
#     
#   classifier = svm.SVC(class_weight='auto', kernel='linear', cache_size=1000)
#   classifier.fit(trainList, classes)  
#   print  'Score: %s' %round(classifier.score(sampleVectors, testClasses), 2)
#     
#   classifier = svm.NuSVC(nu=0.02, kernel='linear', cache_size=1000)
#   classifier.fit(trainList, classes)  
#   print  'Score: %s' %round(classifier.score(sampleVectors, testClasses), 2)
  
  

 
#   if not noOutput: print 'Training...  ',
#   classifier.fit(trainList, classes)  
#   if not noOutput: print 'Done!'
 
  if not noOutput: print 'Saving classifier...  ',
  joblib.dump(classifier, './classifiers/clf_01.pkl')
  if not noOutput: print 'Done!'
  
    
if __name__ == '__main__':
  main()

