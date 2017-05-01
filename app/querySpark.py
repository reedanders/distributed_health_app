import subprocess
import glob
import signal
import re

class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)

def send_query(user, vector):

    tup = (user, vector)
    subprocess.call(["nc", "-lk", "9999", vector])

def parse_output(output):

    parsed = ''
    for file in output:
        f = open(file,'r').read()
        parsed =+ re.findall("\[(.*?)\]",f)
        subprocess.call(["rm",file])

    return parse

def get_result():

    output = []
    path = "/usr/local/spark/output"
    if len(output) == 0:
        output = glob.glob(path)
    else:
        return parse_output(output)

def match(user, vector):

    result = ''
    send_query(user, vector)

    with timeout(seconds=3):
        result = get_result()

    if result == '':
        return 'Spark Failure'
    else:
        return result
