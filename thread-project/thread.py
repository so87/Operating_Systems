#!/usr/bin/env python3

# Simon Owens
# Operating Systems Threading Project
# Dr. Hwang
import sys
import threading
from threading import Thread, Lock
import time
import random

# mutex lock for critical sections of the program
mutex = threading.Lock()


class buffer_item:
    def __init__(self, length):
        self.max_length = length
        self.buffer = []

    # Receives a 'num' to Insert
    # Receives the 'name' of the thread
    def insert_item(self, num, name):
        print("Thread %s waiting to insert an item..." % name)

        # Start of the critical section
        mutex.acquire()
        print("Starting insert_item...")
        print("Thread %s has acquired the CS to insert an item..." % name)
        try:
            # Can't insert the element if the buffer is full
            if(self.max_length == len(self.buffer)):
                print("That element can't be added at max elements...")
                return -1
            # An element was inserted
            else:
                self.buffer.append(num)
                print("Successfully added %d..." % num)
                return 0
        finally:
            print("The buffer is: %s" % self.buffer)
            mutex.release()
            # End of critical section
            print("Thread %s has released the CS...\n\n" % name)

    # Receives a 'num' to remove
    # Receives the 'name' of the thread
    def remove_item(self, num, name):
        print("Thread %s waiting to remove an item..." % name)

        # Start of Critical Section
        mutex.acquire()
        print("Starting remove_item...")
        print("Thread %s has acquired the CS to remove an item..." % name)
        try:
            # Requested element is removed
            if (num in self.buffer):
                self.buffer.remove(num)
                print("Successfully removed %d..." % num)
                return 0
            # The requested element wasn't in the list
            else:
                print("That element %d can't be removed..." % num)
                return -1
        finally:
            print("The buffer is: %s" % self.buffer)
            mutex.release()
            # End of Critical Section
            print("Thread %s has released the CS...\n\n" % name)

# Receives a buffer which contains elements
# Receives the 'name' of the thread


def producer(buffer, name):
    print("Thread %s called the producer function.\n" % name)
    # Keep looping to produce an element until the system stops
    while(1):
        # sleep for a random period of time
        time.sleep(random.randint(1, 10))
        # generate a random number, put in
        random_num = random.randint(1, 10)
        buffer.insert_item(random_num, name)

# Receives a buffer which contains elements
# Receives the 'name' of the thread


def consumer(buffer, name):
    print("Thread %s called the consumer function.\n" % name)
    # Keep looping to consume an element until the system stops
    while(1):
        # sleep for a random period of time
        time.sleep(random.randint(1, 10))
        # generate a random number, put in
        random_num = random.randint(1, 10)
        buffer.remove_item(random_num, name)


def main():
    if(len(sys.argv) != 4):
        print("Usage:\n python3 thread.py sleep-time producer-threads consumer-threads")
        sys.exit()
    print("Starting main...\n")
    # Initilize Buffer
    buffer = buffer_item(5)

    # Get command line arguments argv 1,2,3
    sleep_time = sys.argv[1]
    # Create producer thread(s)
    producer_threads = sys.argv[2]
    for i in range(int(producer_threads)):
        thrd = threading.Thread(group=None, target=producer, name=i, args=(buffer, i))
        # This stops the thread if the main thread stops
        thrd.daemon = True
        print("Producer %s created." % thrd.getName())
        thrd.start()

    # Create comsumer thread(s)
    consumer_threads = sys.argv[3]
    for i in range(int(consumer_threads)):
        thrd = threading.Thread(group=None, target=consumer, name=i, args=(buffer, i))
        # This stops the thread if the main thread stops
        thrd.daemon = True
        print("Consumer %s created." % thrd.getName())
        thrd.start()

    # sleep
    print("Sleeping for %d seconds.\n" % int(sleep_time))
    time.sleep(int(sleep_time))
    # exit
    sys.exit()


if __name__ == "__main__":
    main()
