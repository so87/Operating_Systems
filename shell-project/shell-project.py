#!/usr/bin/env python

# Simon Owens
# Operating Systems
# Dr. Hwang
import os


def child(command):
    if "-" in command:
        args = command.split(" -")
    else:
        args = command.split(" ")

    # get rid of &
    if '&' in args:
        args.remove('&')

    # Do the command
    os.execvp(args[0], args)


def parent(command):
    newpid = os.fork()
    child_pid = 0
    if newpid == 0:                    # child
        # Need to exit when the child gets done
        child_pid = os.getpid()
        # Call a double fork if there is a background process
        if "&" in command:
            newpid = os.fork()
            if newpid == 0:            # grandchild
                child(command)
        else:
            child(command)
        # kill the child process
        os._exit(0)
    else:                              # original parent
        os.waitpid(child_pid, 0)


def main():
    # History for the User
    history = []
    # Loop and accept user commands
    user_input = ""
    while 1:
        user_input = input("osh>")

        # Wants to quit
        if user_input == "quit":
            break

        # user input is blank
        elif user_input == "":
            dumb = 1
        # user wants to enter some command
        else:
            # Wants to see their commands
            if user_input == "history":
                index = len(history)
                for item in history:
                    print("%d %s" % (index, "".join(item)))
                    index -= 1

            # Redoing commands
            elif "!" in user_input:
                user_input = user_input[1:]
                if user_input == "!":
                    parent(history[-1])
                # Need conditional to take care of !N
                else:
                    index = int(user_input)
                    if index <= len(history):
                        parent(history[len(history) - index])
                    else:
                        print ("Sorry, that is not in range\n")

            # A command has been entered
            else:
                history.append(user_input)

                # Make the parent great a child to complete the task
                parent(user_input)


if __name__ == "__main__":
    main()
