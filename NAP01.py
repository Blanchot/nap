#!/usr/bin/python
# NAP_01 Pi Zero standalone
# first test utilizing microdot phat
# URL: https://waterinfo.rws.nl/api/Download/CSV?expertParameter=Waterhoogte___20Oppervlaktewater___20t.o.v.___20Normaal___20Amsterdams___20Peil___20in___20cm&locationSlug=1313&timehorizon=-6,3
# Used script from here:
# https://stackoverflow.com/questions/35371043/use-python-requests-to-download-csv
# Changed delimiter from ',' to ';'
# It looks like I can access what I need with this: my_list[29][4]
# CHANGE: trying my_list[28][4]

'''
4 May 2018 old link stopped working
This is the link to the info:
https://waterinfo.rws.nl/#!/details/publiek/waterhoogte-t-o-v-nap/Rotterdam(ROTT)/Waterhoogte___20Oppervlaktewater___20t.o.v.___20Normaal___20Amsterdams___20Peil___20in___20cm
  
This is the link to the updated .csv file:
https://waterinfo.rws.nl/api/Download/CSV?expertParameter=Waterhoogte___20Oppervlaktewater___20t.o.v.___20Normaal___20Amsterdams___20Peil___20in___20cm&locationSlug=Rotterdam(ROTT)&timehorizon=-6,3

'''
import csv
import requests
import time
from microdotphat import write_string, clear, show

'''
Old url
csv_url = 'https://waterinfo.rws.nl/api/Download/CSV?expertParameter=Waterhoogte___20Oppervlaktewater___20t.o.v.___20Normaal___20Amsterdams___20Peil___20in___20cm&locationSlug=1313&timehorizon=-6,3'
'''

#New url
csv_url = 'https://waterinfo.rws.nl/api/Download/CSV?expertParameter=Waterhoogte___20Oppervlaktewater___20t.o.v.___20Normaal___20Amsterdams___20Peil___20in___20cm&locationSlug=Rotterdam(ROTT)&timehorizon=-6,3'

updatetime = ''
prevlevel = 0

while True:
	try:
		with requests.Session() as s:
			download = s.get(csv_url)
			decoded_content = download.content.decode('utf-8')
			cr = csv.reader(decoded_content.splitlines(), delimiter=';')
			my_list = list(cr)
		#if my_list[29][1] != updatetime and my_list[29][4] != '': #test time changed and level not empty
		if my_list[28][1] != updatetime and my_list[28][4] != '': #test time changed and level not empty
			difflevel = int(my_list[28][4]) - prevlevel #new code to compare and show rise or fall of level
			display = (my_list[28][4] + str('%+d' % difflevel))
			clear()
			write_string(display, kerning=False)
			show()
			updatetime = my_list[28][1]
			prevlevel = int(my_list[28][4]) #new code to compare and show rise or fall of level
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
