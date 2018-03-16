#!/usr/bin/env python3

# Simon Owens and Kunal Mukherjee
# Operating Systems
# Dr. Hwang
# Process Scheduling project


import os
import sys
import time


class process_obj:
	def __init__(self, ID, runtime):
		self.ID = ID
		self.runtime = runtime
		self.state = "ready"
		self.time_left = runtime

	def tick(self):
		self.time_left = int(self.time_left) - 1
		if self.time_left == 0:
			self.state = "terminated"

	def change_state(self, state):
		self.state = state

	def change_wait(self, EID):
		self.wait = EID

	def get_wait(self):
		return self.wait

	def print_self(self):
		return "PID %d %d" % (int(self.ID), int(self.time_left))

	def get_ID(self):
		return self.ID

	def get_timeleft(self):
		return self.time_left

	def get_state(self):
		return self.state

class PCB:
	def __init__(self, q):
		self.ready_list = []
		self.wait_list = []
		self.running_p = process_obj(0, 0)
		self.master_p = None
		self.q = q
		self.q_left = q

	def next_process(self):
		# if there is a next process
		if len(self.ready_list):
			self.running_p = self.ready_list[0]
			self.ready_list.remove(self.running_p)
		# if there isn't
		else:
			self.running_p = process_obj(0,0)

	def update(self):
		# tick - only dec if not PID 0
		if self.running_p.get_ID() != 0:
			self._tick()

		# Put processes where they should go
		# If process is waiting
		if (self.running_p.get_state() == "waiting"):
			self.wait_list.append(self.running_p)
			print ("%s placed on Wait Queue" % self.running_p.print_self())
			self.q_left = self.q
			self.next_process()
		# no time_left to run
		elif (self.running_p.get_timeleft() == 0):
			self.q_left = self.q
			# if master delete everything
			if self.running_p.get_ID() == self.master_p:
				for proc in self.ready_list:
					self.ready_list.remove(proc)
					print ("%s terminated" % proc.print_self())
				for proc in self.wait_list:
					self.wait_list.remove(proc)
					print ("%s terminated" % proc.print_self())
				
			# Remove terminated process and move next thing in 
			self.running_p = process_obj(0,0)
			self.next_process()
		
		# no q_left
		elif (self.q_left == 0):
			self.q_left = self.q
			self.ready_list.append(self.running_p)
			print ("%s placed on the Ready Queue" % self.running_p.print_self())
			self.next_process()	
		# Done putting processes where they should go

		# print out the PCB info 
		self.print_scheduler_info()


	def _tick(self):
		# Decrement q by 1
		self.q_left = int(self.q_left) - 1
		self.running_p.tick()
	
	def create_proc(self, PID, time):
		p = process_obj(PID, time)
		# check to see if this is the master process
		if len(self.ready_list) < 1 and len(self.wait_list) < 1:
			master_ID = p.get_ID() 
		self.ready_list.append(p)
		print("%s placed on Ready Queue" % p.print_self())
		self.update()

	def destroy_proc(self,PID):
		# if that PID is the master destory everything
		if PID == self.master_p:
			for proc in self.ready_list:
				self.ready_list.remove(proc)
				print ("%s terminated" % proc.print_self()) 
			for proc in self.wait_list:
				self.wait_list.remove(proc)
				print ("%s terminated" % proc.print_self())
			self.running_p = process_obj(0,0)
		# check if that proc is current running process
		if PID == self.running_p:
			print ("%s terminated" % self.running_p.print_self())
			self.running_p = process_obj(0,0)

		# check to see if that PID exsists
		else:
			for proc in self.ready_list:
				if proc.get_ID() == PID:
					self.ready_list.remove(proc)
					print ("%s terminated" % proc.print_self())
			for proc in self.wait_list:
				if proc.get_ID() == PID:
					self.wait_list.remove(proc)
					print ("%s terminated" % proc.print_self())
		
		self.update()

	def timer_interrupt(self):
		self.update()

	def wait_event(self,EID):
		if self.running_p.get_ID() == "0":
			print("Cannot execute wait on PID 0")	
		elif EID == "0":
			print("Cannot execute wait of 0 time")
		else:
			self.running_p.change_state("waiting")
			self.running_p.change_wait(EID)
	
		self.update()

	def done_waiting(self, EID):
		# see if any waiting procs have that EID
		for proc in self.wait_list:
			if proc.get_wait() == EID:
				proc.change_state("ready")
				self.ready_list.append(proc)
				self.wait_list.remove(proc)
				print("%s placed on the Ready Queue" % proc.print_self())
		self.update()

	def exit_program(self):
		print("Current state of simulation:")
		self.print_scheduler_info()
	
	def return_str_ready_list(self):
		string = ""
		for item in self.ready_list:
			string += item.print_self() + " "
		return string
	
	def return_str_wait_list(self):
		string = ""
		for item in self.wait_list:
			string += item.print_self() + " " + item.get_wait() + " "
		return string
	
	def print_scheduler_info(self):
		if self.running_p.get_ID() == 0:
			print("PID 0 running")
		else:
			print ("%s running with %d left" % (self.running_p.print_self(), int(self.q_left)))
		print ("Ready Queue: %s" % self.return_str_ready_list())
		print ("Wait Queue: %s" % self.return_str_wait_list())
		print ("")

def main():
	if(len(sys.argv) != 4):
		print ("\nUsage: 'python3 process-scheduler.py input-file q output-file\n")
		sys.exit()
	pcb = PCB(sys.argv[2])
	options = {'C': pcb.create_proc,
            'D': pcb.destroy_proc,
            'I': pcb.timer_interrupt,
            'W': pcb.wait_event,
            'E': pcb.done_waiting,
            'X': pcb.exit_program}
	
	sys.stdout = open(sys.argv[3], 'w')
	print("Simon Owens and Kunal Mukherjee Process Management Class")
	print("------------------------------------")	
	pcb.print_scheduler_info()
	
	# Read line from file for command
	with open(sys.argv[1]) as f:
		for line in f:
			print("%s" % line)
			command = line[0]
			if command == 'C':
				options[command](line[2], line[4:])
			elif command == 'W' or command == 'E' or command == 'D':
				options[command](line[2])
			else:
				options[command]()

if __name__ == "__main__":
	main()
