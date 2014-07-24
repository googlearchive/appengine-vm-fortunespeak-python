from flask import Flask, helpers
import subprocess
import tempfile

from synth import Synth

app= Flask(__name__)
app.debug = True

synth = Synth()

MESSAGES = '/tmp/messages.txt'

@app.route("/")
def fortune():
  msg = subprocess.check_output('/usr/games/fortune')
  with open(MESSAGES, 'a') as f: f.write(msg)
  with tempfile.NamedTemporaryFile() as f:
    synth.say(msg, out=f)
    return helpers.send_file(f.name, mimetype="audio/wav", as_attachment=False)

@app.route("/messages")
def messages():
  return helpers.send_file(MESSAGES)
