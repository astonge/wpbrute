#!/usr/bin/env python

import time
from threading import Thread
import requests
import itertools

THREADS = 16
PASSWORDS = "passwords.txt"

def check_pass(passwords):
	print len(passwords)
	#for i in range(len(passwords)):
	#	if len(passwords[i]) == 0:
	#		print "X"
		#print ":",passwords[i],":"
	#for line in passwords:
    #    print "%s" % (i,line)
    #    time.sleep(2)
    #r = requests.post("http://www.google.com/")
    #print r.text


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

# Fire off worker threads with each chunk.
for i in range(len(password_lines)):
	# send to thread
 	print "[!] Starting Thread..."
	t = Thread(target=check_pass, args=(password_lines[i],))
	t.start()
