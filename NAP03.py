# NAP_3 b7 (added try_except in withPhat and logging for errors)
# Uses 'expected' data rather than 'measured'
# Note because blinkt and microdotphat share methods with the same name we use their full names

import csv
import requests
import time
import blinkt
import microdotphat

import logging
format_string = '%(levelname)s: %(asctime)s: %(message)s'
logging.basicConfig(level=logging.INFO, filename='errors.log', format=format_string)

logging.info('Logging Start')

# Rijswaterstaat water level data:
csv_url = 'https://waterinfo.rws.nl/api/Download/CSV?expertParameter=Waterhoogte___20Oppervlaktewater___20t.o.v.___20Normaal___20Amsterdams___20Peil___20in___20cm&locationSlug=Rotterdam(ROTT)&timehorizon=-6,3'

nap_list = []
nextLevels = []
interval_List = (0,10,20,30,40,50) #checks

# for Blinkt brightness, rgb tuples and pixel list
blinkt.set_brightness(0.04)
rise = (0,8,0)
fall = (32,0,0)
same = (0,0,192)
pixels = (0,1,2,3,4,5,6,7)

def getNap():
  global nap_list
  try:
    with requests.Session() as s:
      download = s.get(csv_url)
      decoded_content = download.content.decode('utf-8')
      cr = csv.reader(decoded_content.splitlines(), delimiter=';')
      nap_list = list(cr)
      return nap_list
  except IndexError:
    microdotphat.clear()
    microdotphat.write_string('IndEr1', kerning=False)
    microdotphat.show()
    print('IndexError 1: getNAP')
  except ConnectionError:
    microdotphat.clear()
    microdotphat.write_string('ConErr', kerning=False)
    microdotphat.show()
    print('ConnectionError: getNAP')

def lookAhead(nap_list,currTime):
  #global prevLevel # not needed for lookAhead
  global nextLevels
  #currTime = input('Current time (hh:mm:ss)? ') #currTime is a str
  #getNap()
  for i in range(len(nap_list)):
    if nap_list[i][1] == currTime:
      currLevel = int(nap_list[i][5]) #currLevel is an int
      prevLevel = int(nap_list[i-1][5])
      #Todo: catch error if prev level in nap_list (Verwachting) is empty
      #Verwachting column is zeroed when an actual value is measured (Meting)
      diffLevel = currLevel - prevLevel
      #print(i) #prints line number of csv file
      #print(currTime, str(currLevel),str('%+d' % diffLevel)) #redundant
      #prevLevel = currLevel # not needed for lookAhead
      #print('Ahead: (1)Levels (2)Diffs (3)Lights')
      nextLevels = []
      for j in range(1,9):
        nextLevels.append(int(nap_list[i+j][5]))
      print(nextLevels)
      compareLevels(currLevel,diffLevel)
      #return nextLevels

def compareLevels(currLevel,diffLevel): #diffLevel here is diff between current - last
  global nextLevels
  # LEVEL DIFFS IN DIGITS
  levelDiffs = [nextLevels[0]-currLevel] #start list with diff between next - current
  for i in range(1,8):
    levelDiffs.append(nextLevels[i]-nextLevels[i-1])
  print(levelDiffs)
  # LEVEL LIGHTS FULL (+,-,=)
  levelLightsFull = []
  '''
  for i in levelDiffs:
    if i > 0:
      levelLightsFull.append('+')
    elif i < 0:
      levelLightsFull.append('-')
    elif i == 0:
      levelLightsFull.append('=')
  '''
  # changed same (or stagnant parameters)
  for i in levelDiffs:
    if i > 1:
      levelLightsFull.append('+')
    elif i < -1:
      levelLightsFull.append('-')
    elif i == 0 or i == 1 or i == -1:
      levelLightsFull.append('=')
  
  #print(levelLightsFull) #prints +, - and =
  setLights(levelLightsFull)
  # LEVEL LIGHTS MINIMAL
  #levelLightsMin = []

def setLights(levelLightsFull):
  blinkt.clear()
  for i in pixels:
    if levelLightsFull[i] == '+':
      blinkt.set_pixel(i,*rise)
    elif levelLightsFull[i] == '-':
      blinkt.set_pixel(i,*fall)
    elif levelLightsFull[i] == '=':
      blinkt.set_pixel(i,*same)
  blinkt.show()


# New code with try/except block
def withPhat():
  while True:
    tijd = time.localtime() #create a struct_time object
    if tijd[4] in interval_List: #and check if the number of minutes is in the interval_List
      currTime = time.asctime()[11:16] #if yes create an hour and minute string using .asctime
      currTime = currTime +':00' #add the zeros
      
      getNap() #get and set current nap_list
      # walk through it searching match with currTime nap_list[i][1]
      # for i in nap_list: doesn't work in this case (because I need the index number?)
      for i in range(len(nap_list)):
        try:
          if nap_list[i][1] == currTime:
            currLevel = int(nap_list[i][5]) #currLevel is an int
            prevLevel = int(nap_list[i-1][5])
            diffLevel = currLevel - prevLevel
            #print(str('%+d' % diffLevel)) #+d formatting for pos and neg numbers
            print(currTime, str(currLevel),str('%+d' % diffLevel))
            # Microdot Phat code follows
            display = str(currLevel) + str('%+d' % diffLevel)
            microdotphat.clear()
            microdotphat.write_string(display, kerning=False)
            microdotphat.show()
            lookAhead(nap_list,currTime) #send nap_list to lookAhead
        except IndexError:
          microdotphat.clear()
          microdotphat.write_string('IndEr2', kerning=False)
          microdotphat.show()
          logging.info('IndexError 2 in withPhat')
          print('IndexError 2 in withPhat')
          time.sleep(65) #not sure how long to wait
          continue #does this work here?
        
    time.sleep(65) # waits a bit more than a minute to escape if = true
  time.sleep(5)


withPhat()


''' # Code without try/except block
def withPhat():
  while True:
    tijd = time.localtime() #create a struct_time object
    if tijd[4] in interval_List: #and check if the number of minutes is in the interval_List
      currTime = time.asctime()[11:16] #if yes create an hour and minute string using .asctime
      currTime = currTime +':00' #add the zeros
      
      getNap() #get and set current nap_list
      # walk through it searching match with currTime nap_list[i][1]
      # for i in nap_list: doesn't work in this case (because I need the index number?)
      for i in range(len(nap_list)):
        if nap_list[i][1] == currTime:
          currLevel = int(nap_list[i][5]) #currLevel is an int
          prevLevel = int(nap_list[i-1][5])
          diffLevel = currLevel - prevLevel
          #print(str('%+d' % diffLevel)) #+d formatting for pos and neg numbers
          print(currTime, str(currLevel),str('%+d' % diffLevel))
          # Microdot Phat code follows
          display = str(currLevel) + str('%+d' % diffLevel)
          microdotphat.clear()
          microdotphat.write_string(display, kerning=False)
          microdotphat.show()
          lookAhead(nap_list,currTime) #send nap_list to lookAhead
        
      time.sleep(65) # waits a bit more than a minute
    time.sleep(5)

'''

'''
Latest Error 2018.06.22

Traceback (most recent call last):
 	File "NAP03.py", line 166, in <module>
 		withPhat()
	File "NAP03.py", line 149, in withPhat
		if nap_list[i][1] == currTime:
IndexError: list index out of range

'''

'''
# No phat code (keep around for testing in Pythonista)
def noPhat():
  while True:
    tijd = time.localtime() #create a struct_time object
    if tijd[4] in interval_List: #and check if the number of minutes is in the interval_List
      currTime = time.asctime()[11:16] #if yes create an hour and minute string using .asctime
      currTime = currTime +':00' #add the zeros
      
      getNap() #get and set current nap_list
      # walk through it searching match with currTime nap_list[i][1]
      # for i in nap_list: doesn't work in this case (because I need the index number?):
      for i in range(len(nap_list)):
        if nap_list[i][1] == currTime:
          currLevel = int(nap_list[i][5]) #currLevel is an int
          prevLevel = int(nap_list[i-1][5])
          diffLevel = currLevel - prevLevel
          #print(str('%+d' % diffLevel)) #+d formatting for pos and neg numbers
          print(currTime, str(currLevel),str('%+d' % diffLevel))
      time.sleep(65) # waits a bit more than a minute
    time.sleep(5)
'''
