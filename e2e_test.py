import logging
import requests
import sys
import time

import sys
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

#HOST = 'http://localhost:5000'
HOST = 'http://silver-python2.appspot.com'
response = requests.get("{}/publish".format(HOST))
task_id = response.content

SLEEP_DURATION_S = 5
logging.info("Waiting for {} seconds".format(SLEEP_DURATION_S))
time.sleep(SLEEP_DURATION_S)

response = requests.get("{}/status/{}".format(HOST, task_id))
assert(response.content == "PROCESSED")



