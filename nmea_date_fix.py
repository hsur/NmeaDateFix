#!/usr/bin/env python3
# vim:fenc=utf-8 ff=unix ft=python ts=4 sw=4 sts=4 noet :

import os
import sys
import datetime
from pynmea2 import NMEASentence, ParseError

if len(sys.argv) != 2:
	print("Usage: %s nmeafile.nmea" % sys.argv[0] )
	sys.exit(1)

file_path = os.path.abspath(sys.argv[1])
tmp_path = os.path.dirname(file_path) + "/updated_" + os.path.basename(file_path)
start_datetime = None

with open(file_path) as f:
	with open(tmp_path, mode='w',newline="\r\n") as t:
		for line in f:
			try:
				nmea = NMEASentence.parse(line)
				if hasattr(nmea, 'datestamp'):
					nmea.datestamp = (nmea.datestamp + datetime.timedelta(weeks=1024)).strftime("%d%m%y")
					if start_datetime == None:
						start_datetime = nmea.datetime.strftime("%Y%m%d%H%M%S")
				t.write(str(nmea))
				t.write("\n")
				#print(str(nmea))
			except ParseError as e:
				t.write(e.args[0][1])
				#print(str(nmea))

os.rename(tmp_path, os.path.dirname(tmp_path) + "/%s.nma" % start_datetime)
