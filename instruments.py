import visa

#Initializes the lock-in information. 
rm = visa.ResourceManager()
multimeter = rm.get_instrument('GPIB0::2')
lock_in = rm.get_instrument('GPIB0::6')

#Wraps the functions of the multimeter into easy to understand commands.

def multimeter_voltage:
	multimeter.write('MEAS:VOLT:DC? 10,0.003')
	
#Wraps the functions of the lock-in into easy to understand commands.
def lockin_phase(n):
	"""Sets the phase offset of the lock-in. -360.00 < n < 729.99 in degrees"""
	lock_in.write('PHAS ' + str(n))

	

