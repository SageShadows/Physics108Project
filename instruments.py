import visa

#Initializes the lock-in information. 
rm = visa.ResourceManager()
multimeter = rm.get_instrument('GPIB0::2')
lockin = rm.get_instrument('GPIB0::6')
convertsens = [2*10**-9, 5*10**-9, 10*10**-9, 20*10**-9, 50*10**-9, 100*10**-9, 200*10**-9, 500*10**-9, 1*10**-6, 2*10**-6, 5*10**-6, 10*10**-6, 20*10**-6, 50*10**-6, 100*10**-6, 200*10**-6, 500*10**-6, 1*10**-3, 2*10**-3, 5*10**-3, 10*10**-3, 20*10**-3, 50*10**-3, 100*10**-3, 200*10**-3, 500*10**-3, 1];
#Wraps the functions of the multimeter into easy to understand commands.

def multimeter_voltage():
	multimeter.write('MEAS:VOLT:DC? 10,0.003')
	
#Wraps the functions of the lock-in into easy to understand commands.
def lockin_phase(n):
	"""Sets the phase offset of the lock-in. -360.00 < n < 729.99 in degrees"""
	lockin.write('PHAS ' + str(n))

def lockin_timeconstant(n):
	"""Sets the time constant of the lock-in. Consult the lock-in manual for the appropriate integer value for time constant"""
	lockin.write('OFLT ' + str(n))

def lockin_autosensitivity():
	"""Auto-adjusts the sensitivity of the lock-in based off the signal provided."""
	lockin.write('AGAN'); 
	while True:
		currentsens = lockin.ask_for_values('SENS?')
		voltage = lockin.ask_for_values('OUTP ? 3')
		if voltage[0]/convertsens[int(currentsens[0])] > 0.8:
			lockin.write('SENS ' + str(int(currentsens[0]) + 1))
		else: break 

def lockin_measurement():
	"""Returns a single measurement point of voltage and phase shift"""
	return lockin.ask_for_values('SNAP ? 3,4')
	

			





	

