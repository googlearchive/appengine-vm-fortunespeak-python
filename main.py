from flask import Flask, request, helpers, Response, send_file, redirect, url_for
from jinja2 import Template

import subprocess
import tempfile
import os.path
import md5

from synth import Synth

app = Flask(__name__)
synth = Synth()

MESSAGES = '/tmp/messages.txt'
TEMPLATE = Template("""
<html>
<body>
<p>{{fortune}}</p>
<audio src="/sounds/{{wav}}" autoplay controls></audio>
<div>
<a href="/"><button>I'm Feeling Lucky</button></a>
</div>
</body>
</html>
""")

# Local directory for caching fortunes and generated sounds,
# each cached fortune is stored under:
# /tmp/fortunes/<md5(text)>
# /tmp/fortunes/<md5(text)>/message.txt
# /tmp/fortunes/<md5(text)>/sound.wav
CACHE = '/tmp/fortunes'

@app.route('/')
def synth_fortune():
    msg = subprocess.check_output('/usr/games/fortune')
    digest = md5.new(msg).hexdigest()
    path = os.path.join(CACHE, digest)
    if os.path.exists(path):
        return redirect(url_for(serve_fortune, path=digest))
    os.makedirs(path)
    with open(os.path.join(CACHE, digest, 'message.txt'), 'w') as f:
        f.write(msg)
    with open(os.path.join(CACHE, digest, 'sound.wav'), 'w') as f:
        synth.say(msg, out=f)
    return redirect(url_for('serve_fortune', path=digest))

@app.route('/<path:path>')
def serve_fortune(path):
    if not os.path.exists(os.path.join(CACHE, path)):
        # cache miss regenerate a new fortune
        return redirect(url_for('synth_fortune'))
    with open(os.path.join(CACHE, path, 'message.txt')) as f:
        msg = f.read()
    return TEMPLATE.render(fortune=msg, wav=path)

@app.route('/sounds/<path:path>')
def serve_sound(path):
    return send_file(os.path.join(CACHE, path, 'sound.wav'))
