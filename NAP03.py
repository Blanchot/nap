# NAP_3 b1 (first test incorporating blinkt lights)
# Uses 'expected' data rather than 'measured'
# Based originally on script from here:
# https://stackoverflow.com/questions/35371043/use-python-requests-to-download-csv
# Changed delimiter from ',' to ';'

import csv
import requests
import time
import blinkt
import microdotphat
#from microdotphat import write_string, clear, show

csv_url = 'https://waterinfo.rws.nl/api/Download/CSV?expertParameter=Waterhoogte___20Oppervlaktewater___20t.o.v.___20Normaal___20Amsterdams___20Peil___20in___20cm&locationSlug=Rotterdam(ROTT)&timehorizon=-6,3'

nap_list = []
interval_List = (0,10,20,30,40,50)

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
