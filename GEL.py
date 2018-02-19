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
		self.next = next_event
		self.prev = prev_event

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
			self.head = new_event
			return None

		ptr = self.head
		if ptr.time > new_event.time:
			self.head = new_event
			new_event.next = ptr
			ptr.prev = new_event
			return new_event

		while (ptr.next is not None) and (new_event.time > ptr.next.time):
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
		while ptr.next is not None:
			ptr = ptr.next
		return ptr


# math formulas
def generate_arrival_time():
    u = random.random()
    return ((-1 / arrival_rate) * log(1 - u))
def generate_service_time():
    u = random.random()
    return ((-1 / service_rate) * log(1 - u))
def generate_packet():
    return Packet(generate_service_time())


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
	event_list = GEL()

	N = 10000

	for i in range(N):
		event_list.schedule("arrival", generate_arrival_time(), generate_packet())
		#print(event_list.head)
	 	#print(event_list.head.time)

	for i in range(N-1):
	    event = event_list.pop()
	    print(event)
	    #print(event_list)
	    current_time = event.time
	    # print(event.time)
	    if event.type == "arrival":
	        total_packet_queue_length += total_active_packets
	        total_packets += 1
	        event_list.schedule("arrival", current_time + generate_arrival_time(), generate_packet())
	        if total_active_packets == 0:
	            event_list.schedule("departure", current_time + event.packet.service_time, event.packet)
	            total_active_packets += 1
	            if server_busy_start_time == -1:
	                server_busy_start_time = current_time
	        elif (total_active_packets < MAXBUFFER + 1) or (MAXBUFFER == 0):
	            packet_queue.put(event.packet)
	            total_active_packets += 1
	        else:
	            total_dropped_packets += 1
	    elif event.type == "departure":
	        total_active_packets -= 1
	        if total_active_packets == 0:
	            if server_busy_start_time != -1:
	                total_server_busy_time += current_time - server_busy_start_time
	                server_busy_start_time = -1
	        if total_active_packets > 0:
	            next_packet = packet_queue.get()
	            event_list.schedule("departure", current_time + next_packet.service_time, next_packet)

	if server_busy_start_time != -1:
	    total_server_busy_time += current_time - server_busy_start_time

	# results
	print("--------------------------------------")
	print("Server utilization:", end=' ')
	print(total_server_busy_time / current_time)
	print("Average queue length:", end=' ')
	print(total_packet_queue_length / total_packets)
	print("Packet drop rate:", end=' ')
	print(total_dropped_packets / total_packets)
	print("--------------------------------------")
	print("The total number of dropped packets", end=' ')
	print(total_dropped_packets)


