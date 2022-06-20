# log_sys is just a simple logger that uses ANSI terminal
# commands
import time


# Log Critical message
def log_c(script, msg):
  print("\033[1;31;43mCRITICAL: " + script + ": " + msg + "\033[0m")
  

# Log Error message
def log_e(script, msg):
  print("\033[31mERROR: " + script + ": " + msg + "\033[0m")


# Log Warning message
def log_w(script, msg):
  print("\033[33mWARNING: " + script + ": " + msg + "\033[0m")


# Log Info message
def log_i(script, msg):
  print("\033[32mINFO: " + script + ": " + msg + "\033[0m")


# Print_erase code.
def print_del(erase, msg):
  print(("\x08" * erase), end="")
  print(msg, end="")
