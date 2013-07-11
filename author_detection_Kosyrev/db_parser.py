# -*- coding: utf-8 -*-

import urllib
import lxml.html


def parseMessages(pagename):   
  ufile = urllib.urlopen(pagename)
  htmlPage = ufile.read()
  
  # Parse messages from div tag
  doc = lxml.html.document_fromstring(htmlPage)
  parsedTextList = doc.xpath('//div[@class="list_posts"]/text()')

  # Exclude parse error with <br> tag
  tempString = ''          
  for string in parsedTextList:
    tempString +=  string
  parsedTextList = tempString.split('\n')

  # Delete wrong detected messages
  messages = []
  for msg in parsedTextList:
    if len(msg) >= 6:
      messages.append(msg.strip())           
  return messages

def extractMessages(userNum, messageCount):
  messages = []
  while messageCount >= 0:
    adr = 'http://forum.killmepls.ru/index.php?action=profile;u=%d;area=showposts;start=%d' %(userNum, messageCount)
    messages.extend(parseMessages(adr))
    messageCount -= 30
  return messages
    

def main():
  
  # File with 'Username userID userMessageCount' strings
  userListFileName = './params/users.txt'
  userList = {}
  
  userListFile = open(userListFileName, 'rU')
  
  # Extract from file to dict: { 'userName': [userID, messageCount] }
  # !!!BUG: If userName with spaces
  for line in userListFile:
    data = line.split()
    userList[data[0]] = [ int(data[1]), int(data[2]) ]
  userListFile.close()
  
  count = 1 
  for userName in userList:
    print 'Parsing user [%d of %d]...' %( count, len(userList)),
    messages = extractMessages(userList[userName][0], userList[userName][1]) # extractMessages(currentUserID, currentMessageCount)
    
    dataFileName = './parsed_data/data/%s.txt' %userName
    
    f = open(dataFileName, 'w')
    f.write('\n'.join(messages))
    f.close()
    
    count += 1
    print 'Done!'
   
  print 'Parsing finished!'
  

if __name__ == '__main__':
  main()