import RPi.GPIO as GPIO
import time

class Relay():
	def __init__(self,pins=[]):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		self.pins = pins
		self.setup()
		
	def setup(self):
		GPIO.setup(self.pins, GPIO.OUT)
		
	def addPin(self,pin):
		self.pins.append(pin)
		self.update()

	def high(pin):
		GPIO.output(pin,  GPIO.HIGH)
	
	def low(pin):
		GPIO.output(pin,  GPIO.LOW)
			
	def highAll(self):
		for pin in self.pins:
			GPIO.output(pin,  GPIO.HIGH)
	
	def lowAll(self):
		for pin in self.pins:
			GPIO.output(pin,  GPIO.LOW)
	
	def wait(a_sec):
		time.sleep(a_sec)
		
	def clean(self):
		GPIO.cleanup()
		
instance = Relay([18])
instance.highAll()
time.sleep(2)
instance.lowAll()
# instance.clean()
