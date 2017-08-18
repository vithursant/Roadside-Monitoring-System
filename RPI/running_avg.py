#!/usr/bin/python



class RunningAverage:
	
	values = [];
	queue_len = 3;
	speed = 80

	def __init__(self, length=20):
		self.queue_len = length
	
	def show_values(self):
		print self.values

	def add_value(self, value):

		if(len(self.values) >= self.queue_len):
			self.values.pop(0)
		self.values.append(value)

	def running_average(self):
		return (sum(self.values)/float(len(self.values)))

	def calc_speed(self):
		avg = self.running_average()
	        if (avg < 0.5):
			if(self.speed < 100):
				self.speed+=5
        	elif (self.speed > 60):
                	self.speed-=5
        	return self.speed

