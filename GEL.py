class Event():
	"""
	time: time at which event occurs 
	type: arrival event, departure event 
	next_event = pointer to next event 
	prev_event = pointer to previous event
	"""
	def __init__(self, time, packet, event_type, next_event, prev_event):
		self.time = time 
		self.packet = packet
		self.type = event_type 
		self.next_event = next_event
		self.prev_event = prev_event

class Packet():
	def __init__(self, service_time):
		self.service_time = service_time

class GEL():

	def __init__(self):
		self.head = None

	def schedule(self, event_type, time, packet):
		# create new event 
		new_event = Event(time, packet, event_type, None, None)
		# insert into GEL
		self.insert(new_event)
		return 

	def insert(self):
		#insert an event
		return 

	def remove(self):
		# remove the first event
		return 


