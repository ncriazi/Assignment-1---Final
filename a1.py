# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Nick Riazi
# ncriazi@uci.edu
# 14622762
import shlex
from pathlib import Path
from notebook import Notebook
from command_parser import parse_command


def main() -> None:
    """
    The main loop of the program that reads user input, parses commands,
    and delegates them for execution. Continues running until the 'Q' command is issued.
    """
    state = {}

    while True:
        user_input = input()
        command_list = shlex.split(user_input)
        
        #shlex.split() splits the input string into a list of arguments
        #based on whitespace and quotes, handling quoted strings correctly

        if not command_list:
            print("ERROR")
            continue
        #checks if the command_list is empty
        if command_list[0] == "Q":
            
            break
        #checks if the first element of the command_list is "Q"
        else:
            success = parse_command(command_list, state)
            
        #calls the parse_command function with the command_list as an argument
        
if __name__ == "__main__":
    main()
