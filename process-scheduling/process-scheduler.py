#!/usr/bin/env python3

# Simon Owens
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

	def change_runtime(self, runtime):
		self.runtime = runtime

	def change_state(self, state):
		self.state = state

	def print_self(self):
		return "PID %d %d" % (int(self.ID), int(self.runtime))

	def get_ID(self):
		return self.ID

	def get_runtime(self):
		return self.runtime

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

	def update(self):
		print("Beginning one turn cycle")	
		# 1 Do the given command
		# 1 make sure and put that process where they go
		
		# 2 check to see running process
			# if not move first ready to running
	
		# 3 tick - only dec if not PID 0

		# 4 see if current running process needs to be terminated

			# 4a if it does need to be terminated, check if master
			# 4b if it was master delete all other processes

		# 5 decrement q
		# 5a if q==0, put process on ready queue, and move first ready queue process in 			running state

		# print out the PCB info 	
	
	def _tick():
		print("Ticking")
		
		# Decrement q by 1
	
	def create_proc(self, PID, time):
		print("Creating process")
		p = process_obj(PID, time)
		self.update()

	def destroy_proc(self,PID):
		print("Destorying process")
		self.update()

	def timer_interrupt(self):
		print("Interrupting process")
		self.update()

	def wait_event(self,EID):
		print("Wait event called")
		self.update()

	def done_waiting(self, EID):
		print("Done waiting called")
		self.update()

	def exit_program(self):
		print("Terminating program")
		self.update()

	def print_scheduler_info(self):
		# find the current running process
		print ("Ready Queue: ")
		print ("Wait Queue: \n")

def main():
	pcb = PCB(sys.argv[2])
	options = {'C': pcb.create_proc,
            'D': pcb.destroy_proc,
            'I': pcb.timer_interrupt,
            'W': pcb.wait_event,
            'E': pcb.done_waiting,
            'X': pcb.exit_program}
	
	# Read line from file for command
	with open(sys.argv[1]) as f:
		for line in f:
			#time.sleep(1)
			command = line[0]
			if command == 'C':
				options[command](line[2], line[4])
			elif command == 'W' or command == 'E' or command == 'D':
				options[command](line[2])
			else:
				options[command]()

	# When completely done make sure all processes are closed

	print("Done with main")


if __name__ == "__main__":
	main()
