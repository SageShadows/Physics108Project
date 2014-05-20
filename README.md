Physics108Project
=================

Physics 108 Project Code for Instrument Interfacing

This file is a quick summary of what this project seeks to do. 

instruments.py wraps the functions that operate the various instruments through GPIB. You will usually not import this unless you want to simply interact with the instruments and not record data. 

experiment.py 
experiment.py seeks to run the experiment for this Physics 108 project. You can either run this in cmd/Terminal using the following command "python experiment.py minTemp maxTemp tempInterval 'filename' phaseShift timeConstant" (phaseShift and timeConstant parameters are not mandatory), or by importing experiment.py into a Python interpreter and running recordData(), using the same parameters. 

For usage not on David's computer and/or using different GPIB addresses, make sure to do the following: 
1) Install the Agilent Technologies GPIB to USB converter (if not on a desktop).
2) Check the GPIB addresses for all instruments in instruments.py
3) Change the appended path in experiment.py to reflect where instruments.py is located. 
4) Change the savepath of the data to reflect where you want your data to be saved. 