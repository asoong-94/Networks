from collections import deque
from queue import PriorityQueue
from math import log
from random import uniform, randint
import random
import matplotlib.pyplot as plt
import itertools
from GEL import GEL
import matplotlib.pyplot as plt


# math formulas
def generate_arrival_time(arrival_rate):
    u = random.random()
    return ((-1 / arrival_rate) * log(1 - u))
def generate_service_time():
    u = random.random()
    return ((-1 / service_rate) * log(1 - u))
def generate_packet():
    return Packet(generate_service_time())
def generate_packet_length():
	return int(random.uniform(64, 1518)) * 8

class Event():
	"""
	time: time at which event occurs 
	type: arrival event, departure event 
	next_event = pointer to next event 
	prev_event = pointer to previous event
	"""
	def __init__(self, time, packet, event_type, next_event, prev_event, nodes):
		N = nodes
		self.time = time 
		self.packet = packet
		self.next = next_event
		self.prev = prev_event
		self.type = event_type
		self.src = random.randint(1,nodes-1)
		self.dest = random.randint(1,nodes-1)
		while self.dest == self.src:
			self.dest = random.randint(1,nodes-1)

class Packet():
	def __init__(self, service_time):
		self.service_time = service_time
		self.packet_length = generate_packet_length()


class Host():
	def __init__(self, hostID):
		self.ID = hostID
		self.hasToken = False
		self.buffer = []

	def send_packet(self, src_packet, dest, N):	
		"""update global gel with packets if has token"""
		# return a delay time

		numHops = src_packet.src - dest
		if numHops < 0:
			numHops = N - abs(numHops)
		return numHops * 10e-5 

	def receive_packet(self, packet):
		"""checks global gel for packets with matching id"""
		return

class GEL():

	def __init__(self):
		self.head = None

	def schedule(self, nodes, event_type, time, packet):
		# create new event 
		new_event = Event(time, packet, event_type, None, None, nodes)
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
		while ptr.next.next is not None:
			ptr = ptr.next
		ret = ptr.next
		ptr.next = None
		return ret

	def print(self):
		ptr = self.head
		while ptr.next is not None:
			print(ptr.type)
			ptr = ptr.next

def run(arrival_rate, service_rate, throughputs, packetDelays, nodes):
	# STATISTICS
	N = nodes
	num_events = 5000
	total_bytes_transmitted = 0
	total_event_time = 0
	total_packet_delay_time = 0
	num_packets = 0
	num_tokens = 0

	
	# DATA STRUCTURES
	# array of hosts, randomly give 1 host a token 
	hosts = [Host(i) for i in range(N)]
	hosts[random.randint(1,N-1)].hasToken = True

	gel = GEL()
	# populate Gel with random events
	for i in range(num_events):
		# creates new event, puts into GEL 
		if i / random.randint(1,10) == 0:
			# schedule token event
			gel.schedule(N, "token", generate_arrival_time(arrival_rate), generate_packet())
			num_tokens += 1
		# schedule regular packet event
		gel.schedule(N, "packet", generate_arrival_time(arrival_rate), generate_packet())
		num_packets += 1


	for i in range(num_events):
		curr_event = gel.pop()

		if curr_event.type == 'packet':
			# queue it in the corresponding host
			hosts[curr_event.src].buffer.append(curr_event)
			total_bytes_transmitted += curr_event.packet.packet_length
			total_event_time += curr_event.time

		elif curr_event.type == 'token':
			# if token find host that has token, empty its buffer
			for host in hosts:
				if host.hasToken:
					if len(host.buffer) > 0:
						# have packet to send
						frame = host.buffer
						for packet in frame:
							packet_time = host.send_packet(packet, packet.dest, N)
							total_packet_delay_time += packet_time
						host.buffer = []

					# regardless, move the token
					hosts[hosts.index(host)].hasToken = False
					hosts[(hosts.index(host)+1) % N].hasToken = False
				else:
					continue

	throughput = int((total_bytes_transmitted / 8) / total_event_time)
	throughputs.append(throughput)

	propagationDelay = total_packet_delay_time / num_packets
	queueingDelay = (1/(service_rate - arrival_rate)) 
	transmissionDelay = (total_bytes_transmitted / 8) / (100000000)
	totalDelay = propagationDelay + queueingDelay + transmissionDelay
	packetDelays.append(totalDelay)



if __name__ == '__main__':
	service_rate = float(input("Please enter the service rate: "))
	# arrival_rate = float(input("Please enter the arrival rate: "))
	N = [10,25]
	arrival_rates = [0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9]
	prop_delay = 1e-6

	N10_throughputs = []
	N10_packetDelays = []

	N25_throughputs = []
	N25_packetDelays = []

	
	for arrival_rate in arrival_rates:
		run(arrival_rate, service_rate, N10_throughputs, N10_packetDelays, 10)

	
	for arrival_rate in arrival_rates:
		run(arrival_rate, service_rate, N25_throughputs, N25_packetDelays, 25)

	print("10 nodes")
	print("Throughputs")
	print(N10_throughputs)
	print("Avg delays")
	print(N10_packetDelays)
	print("------")
	print("25 nodes")
	print("Throughputs")
	print(N25_throughputs)
	print("Avg delays")
	print(N25_packetDelays)

	####### plotting
	
	plt.plot(arrival_rates, N10_throughputs)
	plt.title("Throughput for 10 machines")
	plt.ylabel("Throughput in bytes/sec")
	plt.xlabel("arrival rates")
	plt.savefig("10-Machines-throughputs.png")
	plt.clf()


	plt.plot(arrival_rates, N25_throughputs)
	plt.title("Throughput for 25 machines")
	plt.ylabel("Throughputs in bytes/sec")
	plt.xlabel("arrival rates")
	plt.savefig("25-Machines-throughputs.png")
	plt.clf()



	plt.plot(arrival_rates, N10_packetDelays)
	plt.title("Average Packet Delays for 10 machines")
	plt.ylabel("Average Packet Delays in seconds")
	plt.xlabel("arrival rates")
	plt.savefig("10-Machines-packetDelays.png")
	plt.clf()

	plt.plot(arrival_rates, N25_packetDelays)
	plt.title("Average Packet Delays for 25 machines")
	plt.ylabel("Average Packet Delays in seconds")
	plt.xlabel("arrival rates")
	plt.savefig("25-Machines-packetDelays.png")
	plt.clf()







