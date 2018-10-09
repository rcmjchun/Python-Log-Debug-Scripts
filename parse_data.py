# -*- coding: utf-8 -*-

# parse_data.py: Python terminal script that takes in event log output from Ublox/Europa App
#				 in Android Studio and cleans/reinterprets data into a csv file.
#				 (e.g.   		python parse_data.py input_file.txt	output_file.csv			  )
#
#
#  - Richard Chun (6/13/18)
#

# ctrl + f3 -> home -> shift + end -> del del 


import sys
import csv 
import string


INT12BIT_MAX = 4096
BYTES_CHANNELS = 9
BYTES_OPENER = 2
HEX_IN_BYTE = 2
STEP_SIZE = 1







test_data = """

"""


def unpack(n):
	if n > (INT12BIT_MAX / 2):
		return n - INT12BIT_MAX
	return n



def run(data):
	file_output = "analysis.csv"
	with open(file_output, 'w') as file_out:
		stream = ""
		file_lines = data.splitlines()
		for line in file_lines:
			if (line.find('<') != -1 and line.find('>') != -1):
				start_index = line.find('<')
				end_index = line.find('>')
				result = line[start_index+1 : end_index]
				result = result.strip() + ' '
				stream += result

		packets = []
		packet_length = (BYTES_CHANNELS + BYTES_OPENER) * HEX_IN_BYTE 
		stream = stream.replace(" ", "")
		for i in range(0, len(stream), packet_length):
			packets.append( stream[i:i+packet_length] )

		packets = packets[:-1: STEP_SIZE]
		for pkt in packets:
			result = ""
			pkt = pkt[BYTES_OPENER*HEX_IN_BYTE:]
			result = (
						str(unpack(int(pkt[0:3],   16))) + ',' + 
						str(unpack(int(pkt[3:6],   16))) + ',' + 
						str(unpack(int(pkt[6:9],   16))) + ',' + 
						str(unpack(int(pkt[9:12],  16))) + ',' + 
						str(unpack(int(pkt[12:15], 16))) + ',' +
						str(unpack(int(pkt[15:18], 16))) + '\n'
					)

			file_out.write(result)


run(test_data)






