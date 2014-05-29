import visa

#Initializes the lock-in information. Check the GPIB addresses! 
rm = visa.ResourceManager()
diodemultimeter = rm.get_instrument('GPIB0::2')
feedbackmultimeter = rm.get_instrument('GPIB0::3')
lockin = rm.get_instrument('GPIB0::6')
keithley = rm.get_instrument('GPIB0::24')
convertsens = [2*10**-9, 5*10**-9, 10*10**-9, 20*10**-9, 50*10**-9, 100*10**-9, 200*10**-9, 500*10**-9, 1*10**-6, 2*10**-6, 5*10**-6, 10*10**-6, 20*10**-6, 50*10**-6, 100*10**-6, 200*10**-6, 500*10**-6, 1*10**-3, 2*10**-3, 5*10**-3, 10*10**-3, 20*10**-3, 50*10**-3, 100*10**-3, 200*10**-3, 500*10**-3, 1];

#Wraps the functions of the diode multimeter into easy to understand commands.
def diodemultimeter_voltage():
	"""Measures the voltage of the multimeter. The range is from -2 V to 2 V and also measures up to 10 microvolts."""
	res = diodemultimeter.ask_for_values('MEAS:VOLT:DC? 2,1E-5')
	return res[0]

#Wraps the functions of the feedback multimeter into easy to understand commands.
def feedbackmultimeter_voltage():
	"""Measures the voltage of the multimeter. The range is from -2 V to 2 V and also measures up to 10 microvolts."""
	res = feedbackmultimeter.ask_for_values('MEAS:VOLT:DC? 2,1E-5')
	return res[0]

def feedbackmultimeter_ACVoltage():
	"""Measures the AC voltage of the multimeter. The range is from -5 V to 5 V and also measures up to 10 microvolts."""
	res = feedbackmultimeter.ask_for_values('MEAS:VOLT:AC? 5,1E-5')
	return res[0]

#Wraps the functions of the lock-in into easy to understand commands.
def lockin_phase(phase):
	"""Sets the phase offset of the lock-in. -360.00 < phase < 719.99 in degrees"""
	lockin.write('PHAS ' + str(phase))

def lockin_timeconstant(n):
	"""Sets the time constant of the lock-in. Consult the lock-in manual for the appropriate integer value for time constant"""
	lockin.write('OFLT ' + str(n))

def lockin_autosensitivity():
	"""Auto-adjusts the sensitivity of the lock-in based off the signal provided."""
	lockin.write('AGAN'); 
	while True:
		currentsens = lockin.ask_for_values('SENS?')
		voltage = lockin.ask_for_values('OUTP ? 3')
		if voltage[0]/convertsens[int(currentsens[0])] > 0.8 and currentsens[0] < 26:
			lockin.write('SENS ' + str(int(currentsens[0]) + 1))
		else: break 

def lockin_measurement():
	"""Returns a single measurement point of voltage and phase shift."""
	return lockin.ask_for_values('SNAP ? 3,4')
	
#Wraps the functions of the Keithley into easy to understand commands. 
def keithley_setvoltage(volt):
	"""Sets the voltage of the Keithley. Enter the voltage in volts. Do not exceed the range of 2.1 V. Accuracy up to 0.1 mV"""
	keithley.write(':SOUR:FUNC VOLT')
	keithley.write(':SOUR:VOLT:MODE FIXED')
	keithley.write(':SOUR:VOLT:RANG 1')
	keithley.write(':SOUR:VOLT:LEV ' + str(volt))
	keithley.write(':SENS:CURR:PROT 0.5E-3')
