#!/usr/bin/env python
import numpy as np
import time
import sys
sys.path.append('C:\Users\David\Desktop\Dropbox\School Work\Physics108Project')
import instruments
import os.path

#Definitions of various mathematical functions and constants.
temptovolt = lambda x: -0.0018*x+1.167 #Converts temperature to voltage for LN2 range.  
volttotemp = lambda y: -555.4*y+648 #Converts voltage to temperature for LN2 range.  
#temptovolt = lambda x: -0.002296*x+1.248 #Converts temperature to voltage for 300K range
#volttotemp = lambda y: -435.6*y+543.7 #Converts voltage to temperature for 300K range
tolerance = 0.01 #Tolerance in volts. 
savepath = 'C:\\Users\\David\\Desktop\\Dropbox\\School Work\\2013-2014\\Spring 2014\\PHYSICS 108'

def recordData(minTemp, maxTemp, tempInterval, filename, phaseShift = 0, timeConstant = 11): 
	""""Temperatures are given in Kelvin. The filename is a string that the data will be saved to. The phase shift is expermentially defined"""
	initializeExperiment(phaseShift, timeConstant)
	data = [['Temperature' 'Voltage' 'Phase']]
	for i in np.linspace(minTemp, maxTemp, (maxTemp - minTemp)/tempInterval + 1):
		refvolt = temptovolt(i);
		instruments.keithley_setvoltage(refvolt)
		thermalEq()
		instruments.lockin_autosensitivity()
		datapoint = instruments.lockin_measurement()
		actualtemp = volttotemp(instruments.diodemultimeter_voltage())
		data.append([actualtemp] + datapoint)
	saveFile(filename, data)

def initializeExperiment(phaseShift, timeConstant):
	"""Initializes the experiment by setting the phase shift and the time constant of the lock-in"""
	instruments.lockin_phase(phaseShift)
	instruments.lockin_timeconstant(timeConstant)

def thermalEq(): 
	counter = 0
	while True: 
		time.sleep(5)
		feedbackvolt = instruments.feedbackmultimeter_voltage()
		if abs(feedbackvolt) < tolerance: counter = counter + 1
		else: counter = 0
		print str(feedbackvolt) + " is the current feedback voltage. " + str(counter) + " is the current counter number."
		if counter == 5: break
	print "Thermal drift stabilized to " + str(tolerance) + " V."

def saveFile(filename, data):
	"""Saves data to a given filename to the path specified in the beginning of this script."""
	completeName = os.path.join(savepath, filename + ".txt")         
	f1 = open(completeName, "w")
	for i in data:
		f1.write('' + str(i[0]) + '\t' + str(i[1]) + '\t' + str(i[2]) + '\n')
	f1.close()

if __name__ == '__main__':
	recordData(*sys.argv[1:])

