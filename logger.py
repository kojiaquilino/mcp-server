import sys
from datetime import datetime

def log_stderr(message: str):
    timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error = timestamp + ": " + message
    print(error, file=sys.stderr, flush=True) # same as sys.stderr.write() with buffer flushing