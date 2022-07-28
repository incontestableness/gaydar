#!/usr/bin/env python3

import os
import sys


print("Hello, world!")

# We need to chdir and update our python path when running as a WSGI application
if __name__ != "__main__":
	# Get the full path to gaydar
	runtime = os.path.expanduser("~/gaydar")
	# Python needs to know where to look for the gaydar module
	sys.path.insert(0, runtime)

# Now we can load gaydar
from gaydar import app as application

# If we're not being run as a WSGI application, start the gaydar API server in the main thread and enable web tracebacks for debugging
if __name__ == "__main__":
	application.debug = True
	print("WARNING: Listening on all available interfaces!")
	application.run(host="0.0.0.0", port=7125) # gay port
