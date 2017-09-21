#!/usr/bin/env python

import requests
import re

url="http://doom:8000/wp-login.php"
user = "admin"
password="Password1234"
regex = ur"<strong>ERROR</strong>"

print "Sending request..."
payload = {'log':user, 'pwd':password,'wp-submit':'Log In'}
r = requests.post(url, data=payload)
#matches = re.finditer(regex,r.text)
match = re.search(regex,r.text)
if match:
    print 'No Match Found'
else:
    print "Match found.."

#for matchNum, match in enumerate(matches):
#    matchNum = matchNum + 1
#    print matchNum
#    print "Invalid login found."
