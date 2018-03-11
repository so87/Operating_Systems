#!/usr/bin/env python

# Simon Owens
# Operating Systems
# Dr. Hwang
# Process Scheduling project


import os
import sys
import time


class process_obj:
  def __init__(self, ID, runtime, q):
    self.ID = ID
    self.runtime = runtime
    self.state = "running"
    self.time_left = runtime
    self.q = q

  def change_runtime(self, runtime):
    self.runtime = runtime

  def change_state(self, state):
    self.state = state

  def tick(self):
    self.q = int(self.q) - 1
    self.time_left = int(self.time_left) - 1
    if self.time_left == 0:
      self.state = "done"

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


def print_scheduler_info(p_list):
	# find the current running process
  	run_p = process_obj(0, 0, 0)
  	for p in p_list:
    		if p.get_state() == "running":
     			run_p = p
	print "%s running with %d left" % (str(run_p.print_self()), int(run_p.get_timeleft()))
        print "Ready Queue: "
        print "Wait Queue: \n"
        run_p.tick()


def create_proc(PID, time, q):
  print("Creating process")
  p = process_obj(PID, time, q)
  return p

def destroy_proc(PID):
  print("Destorying process")


def timer_interrupt():
  print("Interrupting process")


def wait_event(EID):
  print("Wait event called")


def done_waiting(EID):
  print("Done waiting called")


def exit_program():
  print("Terminating program")


def main():
  options = {'C': create_proc,
             'D': destroy_proc,
             'I': timer_interrupt,
             'W': wait_event,
             'E': done_waiting,
             'X': exit_program}
  p_list = []
  q = sys.argv[2]

  # Read line from file for command
  with open(sys.argv[1]) as f:
	for line in f:
      	  time.sleep(1)
          command = line[0]
          if command == 'C':
         	p_list.append(options[command](line[2], line[4], q))
       	  elif command == 'W' or command == 'E' or command == 'D':
          	options[command](line[2])
          else:
          	options[command]()

          # Print out info
          print_scheduler_info(p_list)

  # When completely done make sure all processes are closed

  print("Done with main")


if __name__ == "__main__":
  main()
