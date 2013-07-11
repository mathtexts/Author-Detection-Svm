# -*- coding: utf-8 -*-

from os import listdir
from os.path import isfile, join
from random import randrange

from toolkit import readMessagesFromFile

def main():
  
  dataPath = './parsed_data/data'
  
  fileList = [ f for f in listdir(dataPath) if isfile(join(dataPath,f)) ]
  
  for fileName in fileList:
    messages = readMessagesFromFile(join(dataPath, fileName))
    
    traindbFileName = './parsed_data/db/%s' %fileName
    testdbFileName = './parsed_data/test_db/%s' %fileName
    
    trainMessages = []
    testMessages = []
    for i in range(len(messages)):
      if randrange(100) < 10:
        testMessages.append(messages[i])
      else:
        trainMessages.append(messages[i])
#         if len(trainMessages) > 1000: break
    
    # Statistics:    
    mean = [ len(msg) for msg in messages ]
    print '%s: %s %s %s %s' %( fileName[:-4], len(messages), len(trainMessages), len(testMessages), round( sum(mean)/float(len(mean)), 1 ) )
    
    f1 = open(traindbFileName, 'w')
    f1.write('\n'.join(trainMessages))
    f1.close()
     
    f2 = open(testdbFileName, 'w')
    f2.write('\n'.join(testMessages))
    f2.close()
    
#     print len(testMessages), len(trainMessages)
    
if __name__ == '__main__':
  main()