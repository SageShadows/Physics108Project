#!/usr/bin/env python
import numpy as np
import time
import sys
sys.path.append('C:\Users\David\Desktop\Dropbox\School Work\Physics108Project')
import instruments
import os.path
import datetime

#Definitions of various mathematical functions and constants.
temptovolt = lambda x: -0.0018*x+1.167 #Converts temperature to voltage for LN2 range.  
volttotemp = lambda y: -555.4*y+648 #Converts voltage to temperature for LN2 range.  v
#temptovolt = lambda x: -0.002296*x+1.248 #Converts temperature to voltage for 300K range
#volttotemp = lambda y: -435.6*y+543.7 #Converts voltage to temperature for 300K range
temperror  = lambda z: 0.06339902*(1+1/8+((z-1.0121275)**2)/0.00059121) #error on temperature as function of voltage in LN2 range
tolerance = 0.01 #Tolerance in volts. 
thermalLoopConstant = 60 #Number of times we loop for the thermal error check. 
savepath = 'C:\\Users\\David\\Desktop\\Dropbox\\School Work\\2013-2014\\Spring 2014\\PHYSICS 108'

def recordDataSimple(filename, phaseShift = 0, timeConstant = 7):
	initializeExperiment(phaseShift, timeConstant)
	data = ['Time','Temperature', 'TempError','Voltage','Phase', 'Solenoid Voltage']
	completeName = os.path.join(savepath, filename + ".txt")         
	f1 = open(completeName, "w")
	while(True):
		f1.write(str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "," + str(data[3]) + "," + str(data[4]) + str(data[5]) + "\n")
		TempVoltage = ((-1)*instruments.diodemultimeter_voltage())
		instruments.lockin_autosensitivity()
		datapoint = instruments.lockin_measurement()
		data[0] = datetime.datetime.now()
		data[1] = volttotemp(TempVoltage)
		data[2] = temperror(TempVoltage)
		data[3] = datapoint[0]
		data[4] = datapoint[1]
		data[5] = instruments.feedbackmultimeter_ACVoltage()
		if data[1] > 100:
			break
	f1.close()


def recordData(minTemp, maxTemp, tempInterval, filename, phaseShift = 0, timeConstant = 11): 
	""""Temperatures are given in Kelvin. The filename is a string that the data will be saved to. The phase shift is expermentially defined"""
	initializeExperiment(phaseShift, timeConstant)
	data = [['Temperature','Voltage','Phase']]
	tempData = [['Temperature', 'Error']]
	for temp in np.linspace(minTemp, maxTemp, (maxTemp - minTemp)/tempInterval + 1):
		print(temp)
		thermalEq(temp)
		tempData.append(thermalError())
		instruments.lockin_autosensitivity()
		datapoint = instruments.lockin_measurement()
		actualtemp = volttotemp(-1*instruments.diodemultimeter_voltage())
		print [actualtemp] + datapoint
		data.append([actualtemp] + datapoint)
	CSVData(data, tempData, filename + "AndreVersion")
	saveFile3(filename, data)
	#saveFile2(filename + "TempError", tempData)

def initializeExperiment(phaseShift, timeConstant):
	"""Initializes the experiment by setting the phase shift and the time constant of the lock-in"""
	instruments.lockin_phase(phaseShift)
	instruments.lockin_timeconstant(timeConstant)

def thermalEq(temp): 
	refvolt = temptovolt(temp)
	instruments.keithley_setvoltage(refvolt)
	counter = 0
	while True: 
		time.sleep(1) #higher resolution
		feedbackvolt = instruments.feedbackmultimeter_voltage()
		if abs(feedbackvolt) < tolerance: counter = counter + 1
		else: counter = 0
		print str(feedbackvolt) + " is the current feedback voltage. " + str(counter) + " is the current counter number."
		if counter == 25: break #better convergence criterion
	print "Thermal drift stabilized to " + str(tolerance) + " V."

def thermalError():
		result = []
		for i in np.arange(thermalLoopConstant):
			time.sleep(1)
			voltage = -1*instruments.diodemultimeter_voltage()
			actualtemp = volttotemp(voltage)
			error = temperror(voltage)
			result.append([actualtemp, error])
		return result
	
def takeSingleMeasurement():
	instruments.lockin_autosensitivity()
	datapoint = instruments.lockin_measurement()
	actualtemp = volttotemp(-1*instruments.diodemultimeter_voltage())
	return [actualtemp] + datapoint

def CSVData(data, tempData, name):
	completeName = os.path.join(savepath, name + ".txt") 
	f1 = open(completeName, "w")
	for i in np.arange(1,len(data)):
		result = str(data[i][1]) + ", " + str(data[i][2])
		tempstring = ""
		errstring = ""
		for j in range(thermalLoopConstant):
			tempstring = tempstring + ", " + str(tempData[i][j][0])
			errstring = errstring + ", " + str(tempData[i][j][1])
		result = result + tempstring + errstring + "\n"
		f1.write(result)
	f1.close()

def saveFile3(filename, data):
	"""Saves data to a given filename to the path specified in the beginning of this script for 3 data points."""
	completeName = os.path.join(savepath, filename + ".txt")         
	f1 = open(completeName, "w")
	for i in data:
		f1.write(str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + "\n")
	f1.close()

def saveFile2(filename, data):
	"""Saves data to a given filename to the path specified in the beginning of this script for 2 data points. """
	completeName = os.path.join(savepath, filename + ".txt")         
	f1 = open(completeName, "w")
	for i in data:
		f1.write(str(i[0]) + "," + str(i[1]) + "," + "\n")
	f1.close()

if __name__ == '__main__':
	recordData(*sys.argv[1:])
