# NAP_3 b3 (first test incorporating blinkt lights)
# Uses 'expected' data rather than 'measured'
# Based originally on script from here:
# https://stackoverflow.com/questions/35371043/use-python-requests-to-download-csv
# Changed delimiter from ',' to ';'

#NOTE: NEED TO DIFFERENTIATE BETWEEN MICRODOTPHAT AND BLINKT METHODS

import csv
import requests
import time
import blinkt
import microdotphat
#from microdotphat import write_string, clear, show
 

csv_url = 'https://waterinfo.rws.nl/api/Download/CSV?expertParameter=Waterhoogte___20Oppervlaktewater___20t.o.v.___20Normaal___20Amsterdams___20Peil___20in___20cm&locationSlug=Rotterdam(ROTT)&timehorizon=-6,3'

nap_list = []
nextLevels = []
interval_List = (0,10,20,30,40,50)

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
    microdotphat.write_string('IndErr', kerning=False)
    microdotphat.show()
    print('Index Error')
  except ConnectionError:
    microdotphat.clear()
    microdotphat.write_string('ConErr', kerning=False)
    microdotphat.show()
    print('Connection Error')

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
      print('Ahead: (1)Levels (2)Diffs (3)Lights')
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
  for i in levelDiffs:
    if i > 0:
      levelLightsFull.append('+')
    elif i < 0:
      levelLightsFull.append('-')
    elif i == 0:
      levelLightsFull.append('=')
  print(levelLightsFull)
  # LEVEL LIGHTS MINIMAL
  #levelLightsMin = []

'''
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

#noPhat()
withPhat()

'''
while True:
  try:
    with requests.Session() as s:
      download = s.get(csv_url)
      decoded_content = download.content.decode('utf-8')
      cr = csv.reader(decoded_content.splitlines(), delimiter=';')
      my_list = list(cr)
    if my_list[29][1] != updatetime and my_list[29][4] != '': #test time changed and level not empty
      difflevel = int(my_list[29][4]) - prevlevel #new code to compare and show rise or fall of level
      display = (my_list[29][4] + str('%+d' % difflevel)) #+d formatting for positive and neg numbers 
      clear()
      write_string(display, kerning=False)
      show()
			updatetime = my_list[29][1]
			prevlevel = int(my_list[29][4]) #new code to compare and show rise or fall of level
		time.sleep(300) # waits 5 minutes
	except IndexError:
		clear()
		write_string('IndErr', kerning=False)
		show()
		time.sleep(300)
	#except ConnectionError:
		#clear()
		#write_string('ConErr', kerning=False)
		#show()
		#time.sleep(300)

'''
