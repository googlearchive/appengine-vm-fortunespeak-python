from pyttsx.drivers import _espeak
import ctypes
import wave
import time
import threading
import StringIO

class Synth(object):
    _done = False
    def __init__(self):
        self.rate = _espeak.Initialize(_espeak.AUDIO_OUTPUT_RETRIEVAL, 1000)
        assert self.rate != -1, 'could not initialize espeak'
        _espeak.SetSynthCallback(self)
        self.lock = threading.Lock()

    def __call__(self, wav, numsamples, events):
        if self._done:
            return 0
        data = ctypes.string_at(wav, numsamples*2)
        if len(data) == 0:
            self._done = True
            return 0
        self.wav.writeframes(data)
        return 0

    def say(self, say, out):
        with self.lock:
            self.wav = wave.open(out, 'w')
            self.wav.setnchannels(1)
            self.wav.setsampwidth(2)
            self.wav.setframerate(self.rate)
            self._done = False
            _espeak.Synth(say)
            while not self._done:
                time.sleep(0)
            self.wav.close()
