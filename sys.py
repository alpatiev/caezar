import os

# Get system information
system_info = os.uname()

# Extract nodename from system_info tuple
nodename = system_info.nodename

print("Nodename:", nodename)

