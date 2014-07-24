from flask import Flask, helpers
import subprocess

app = Flask(__name__)

MESSAGES = '/tmp/messages.txt'

@app.route("/")
def fortune():
  msg = subprocess.check_output('/usr/games/fortune')
  with open(MESSAGES, 'a') as f: f.write(msg)
  return msg

@app.route("/messages")
def messages():
  return helpers.send_file(MESSAGES)