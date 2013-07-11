# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, join



class BagOfWords(object):
  """ Implementing a bag of words, words corresponding with their frequency of usages in a "document"
  for usage by the Document class, DocumentClass class and the Pool class."""
  
  def __init__(self):
    self.__number_of_words = 0
    self.__bag_of_words = {}
    
  def __add__(self,other):
    """ Overloading of the "+" operator to join two BagOfWords """
    erg = BagOfWords()
    _sum = erg.__bag_of_words
    for key in self.__bag_of_words:
      _sum[key] = self.__bag_of_words[key]
      if key in other.__bag_of_words:
        _sum[key] += other.__bag_of_words[key]
    for key in other.__bag_of_words:
      if key not in _sum:
        _sum[key] = other.__bag_of_words[key]
    return erg
      
  def add_word(self,word):
    """ A word is added in the dictionary __bag_of_words"""
    self.__number_of_words += 1
    if word in self.__bag_of_words:
      self.__bag_of_words[word] += 1
    else:
      self.__bag_of_words[word] = 1
  
  def len(self):
      """ Returning the number of different words of an object """
      return len(self.__bag_of_words)
  
  def Words(self):
    """ Returning a list of the words contained in the object """
    return self.__bag_of_words.keys()
  
      
  def BagOfWords(self):
    """ Returning the dictionary, containing the words (keys) with their frequency (values)"""
    return self.__bag_of_words
      
  def WordFreq(self,word):
    """ Returning the frequency of a word """
    if word in self.__bag_of_words:
      return self.__bag_of_words[word]
    else:
      return 0



def extractTopWords(text):
  ''' Returning list of words, used in text, sorted by frequency '''
  
  bagOfWords = BagOfWords()
  message = text.split()
  for word in message:
    bagOfWords.add_word(word)
  
  bog = bagOfWords.BagOfWords()
  lst = []
  # Sorted by values: word freq
  for key, value in sorted(bog.iteritems(), key=lambda (k,v): (v,k), reverse = True):
    lst.append((key, value))
    
  return lst

def readMessagesFromFile(fileName):
  '''Returning list of messages, extracted from fileName and splitted by '\n' '''
  
  contentFile = open(fileName, 'rU')
  text = contentFile.read()
  contentFile.close()
  
  return text.split('\n')

def trimMessageList(messageList, lenght):
  ''' Returning list of messages, with short messages removed '''
  
  msgList = []
  for message in messageList:
    if len(message) > lenght: msgList.append(message)
  return msgList

class Vectorizer(object):
  
  def __init__(self, dbPath, vectorSize):
    self.sizeOfVector = vectorSize
    self.glDict = {}
    self.classMap = {}
    self.dbPath = dbPath
    
    classMapPath = './params/classmap.txt'
    
    if isfile(self.dbPath) and 'globaldict.txt' in self.dbPath:
      self.glDict = self.loadGlobalDict(self.dbPath)
      self.classMap = self.loadClassMap(classMapPath)
    else:
      self.classMap = self.createClassMap(dbPath)
      self.saveClassMap(classMapPath)
      self.glDict = self.createGlobalDict()
      self.saveGlobalDictToFile('./params/globaldict.txt')
      
  
  def getVect(self, message):
    locDict = {}
    for key in sorted(self.glDict.keys()):
      locDict[key] = [ 0 for i in range(len(self.glDict[key])) ]
    
    topWords = extractTopWords(message)
    for word in topWords:
      for userName in sorted(self.glDict.keys()):
        if word[0] in self.glDict[userName]: 
          locDict[userName][self.glDict[userName].index(word[0])] = word[1]
  
    vect = []
    for userName in sorted(locDict.keys()):
      vect.extend(locDict[userName])
    
    return vect
  
  def getClassMap(self):
    return self.classMap
  
  
  def createClassMap(self, dbPath):
    '''Returning dictionary with { key=userID : value=authorName } from ./db/ folder'''
    
    fileList = [ f for f in listdir(dbPath) if isfile(join(dbPath,f)) ]
    usersDict = {}
    for k in range(len(fileList)):
      fileName = fileList[k]
      if '.txt' in fileName:
        usersDict[k] = fileName[:-4]
    return usersDict
  
  def saveClassMap(self, path):
    lst = []
    for key in sorted(self.classMap.keys()):
      lst.append( ' '.join( [str(key), self.classMap[key]] ) )
    f = open(path, 'w')
    f.write('\n'.join(lst))
    f.close()
      
  def loadClassMap(self, path):
    classMap = {}
    lst = self.readMessagesFromFile(path)
    for line in lst:
      classId, className = line.split()
      classMap[int(classId)] = className
    return classMap

  
  def createGlobalDict(self):
    glDict = {}
    for userID in sorted(self.classMap.keys()):
      userName = self.classMap[userID]
      fileName = '%s%s.txt' %(self.dbPath, userName)
      text = open(fileName ,'rU').read()
      lst = extractTopWords(text)
      if len(lst) > self.sizeOfVector : del lst[self.sizeOfVector:]
      glDict[userName] = [ word[0] for word in lst ]
    return glDict
  
  def saveGlobalDictToFile(self, path):
    lst = []
    for key in sorted(self.glDict.keys()):
      lst.append(str(key) + ' ' + ' '.join(self.glDict[key]))
    f = open(path, 'w')
    f.write('\n'.join(lst))
    f.close()
    
  def loadGlobalDict(self, path):
    glDict = {}
    lst = self.readMessagesFromFile(path)
    for line in lst:
      words = line.split()
      glDict[words[0]] = words[1:]
    return glDict
  

  def readMessagesFromFile(self, fileName):
    '''Returning list of messages, extracted from fileName and splitted by '\n' '''
  
    contentFile = open(fileName, 'rU')
    text = contentFile.read()
    contentFile.close()
    return text.split('\n')
  
  
  

def getClassificationData(dbPath, vectorSize, msgLen):
  ''' Returning list of vectors and list of corresponding classes for SVM.
      Generates from all files, founded in dbPath '''
  
  # Read dict with numbered top used words from 'globaldict.txt'
#   globalDict = getGlobalDict()
  
  # Dict with numbered users(generated by *.txt files in dbPath folder)
  # User ID = class number for SVM
  if dbPath == './db/':
    gl = Vectorizer('./db/', vectorSize)
  else:
    gl = Vectorizer('./params/globaldict.txt', vectorSize)
  clMap = gl.getClassMap()
 
  vectors = []
  classes = []
  fileList = [ f for f in listdir(dbPath) if isfile(join(dbPath,f)) ]
  for fileName in sorted(fileList):  
    messageList = readMessagesFromFile(join(dbPath, fileName))
    # Filter message lenght
    messageList = trimMessageList(messageList, msgLen)
    
    for userID, userName in clMap.items():
      if userName in fileName: classID = userID
      
    for message in messageList:
      vectors.append( gl.getVect(message) )
      classes.append(classID)
  return vectors, classes 
