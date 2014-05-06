import visa

#Initializes the lock-in information. 
rm = visa.ResourceManager()
multimeter = rm.get_instrument('GPIB0::2')
lock_in = rm.get_instrument('GPIB0::6')

#Sets 
def phase(n):
	"""Sets the phase offset of the lock-in. -360.00 < n < 729.99 in degrees"""
	lock_in.write('PHAS ' + str(n))

	

