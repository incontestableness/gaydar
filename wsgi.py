#!/usr/bin/env python3

import os
import sys


print("Hello, world!")

# We need to chdir and update our Python path when running as a WSGI application
if __name__ != "__main__":
	# Get the full path to gaydar
	runtime = os.path.expanduser("~/gaydar")
	# Python needs to know where to look for the gaydar module
	sys.path.insert(0, runtime)

# Now we can load gaydar
from gaydar import app as application

# If we're not being run as a WSGI application, start the gaydar API server in the main thread
if __name__ == "__main__":
	print("WARNING: Listening on all available interfaces!")
	# Enable tracebacks and web debugging, but don't use the autoreloader as it can cause issues
	# app.debug enables both
	application.run(use_debugger=True, use_reloader=False, host="0.0.0.0", port=7125) # gay port
