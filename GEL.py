from math import log
import random
import queue

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

	def insert(self, new_event):
		#insert an event
		if self.head is None:
			self.head = next_event
			return None

		ptr = self.head
		if ptr.time > new_event.time:
			self.head = new_event
			new_event.next = ptr
			ptr.prev = new_event
			return new_event

		while ptr.next is not None and new_event.time > ptr.next.time:
			ptr = ptr.next

		new_event.prev = ptr
		new_event.next = ptr.next
		ptr.next = new_event

		if new_event.next:
			new_event.next.prev = new_event

		return new_event

	def pop(self):
		# remove the first event
		if self.head is None:
			return None

		ptr = self.head
		while ptr.next_event is not None:
			ptr = ptr.next_event
		return 

if __name__ == '__main__':
	# configurations
	MAXBUFFER = int(input("Please enter the MAXBUFFER size for the packets queue: "))
	service_rate = float(input("Please enter the service rate: "))
	arrival_rate = float(input("Please enter the arrival rate: "))

	# statistics
	total_server_busy_time = 0
	total_packet_queue_length = 0
	total_packets = 0
	total_active_packets = 0
	total_dropped_packets = 0

	current_time = 0
	server_busy_start_time = -1

	# initialize
	packet_queue = queue.Queue(MAXBUFFER)
	event_list = GEL.GEL()

