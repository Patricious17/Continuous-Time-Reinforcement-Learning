#!/usr/bin/python

class Controller:
	def __init__(self, control_):
		self.control = control_ # control is a 'callable object'
		self.controlValue = 0.0 # do not apply any control initially

	def __call__(self, *args, **kwargs):
		if 'error' in kwargs:
			self.updateControlValue(kwargs['error'])
		return self.controlValue

	def updateControlValue(self, error):
		self.controlValue = self.control(error)

# here we implement PID as a callable object
class PID:
	def __init__(self, proportionalGain_, derivativeGain_ = 0.0):
		self.proportionalGain = proportionalGain_
		self.derivativeGain	= derivativeGain_

	def __call__(self, *args, **kwargs):
		error = kwargs['error']
		control = 0.0 # default return value to 0.0

		# implement pid controller using numpy here

		return control

	def setGains(self, proportionalGain_ = None, derivativeGain_ = None):
		if proportionalGain_ is not None:
			self.proportionalGain = proportionalGain_
		if derivativeGain_ is not None:
			self.derivativeGain = derivativeGain_


#implement unit tests here
def test1():
	print('Running test1...')
	pid = PID(0.1, 0.05)
	assert pid.proportionalGain == 0.1
	assert pid.derivativeGain == 0.05
	ctrl = Controller(pid)
	assert ctrl(0.0) == 0.0
	pid.setGains(0.5, 0.4)
	assert ctrl.control.proportionalGain == 0.5 and ctrl.control.derivativeGain == 0.4
	#add more tests to test functionality of PID
	print('Test1 completed!')
