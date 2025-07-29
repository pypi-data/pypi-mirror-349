from collections import deque
from threading import Event, Lock

import numpy as np
import sounddevice as sd


class AudioPlayer:
    def __init__(self, sample_rate=24_000, buffer_size=2048):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.audio_buffer = deque()
        self.buffer_lock = Lock()
        self.playing = False
        self.drain_event = Event()

    def callback(self, outdata, frames, time, status):
        outdata.fill(0)  # initialize the frame with silence
        filled = 0

        with self.buffer_lock:
            while filled < frames and self.audio_buffer:
                buf = self.audio_buffer[0]
                to_copy = min(frames - filled, len(buf))
                outdata[filled : filled + to_copy, 0] = buf[:to_copy]
                filled += to_copy

                if to_copy == len(buf):
                    self.audio_buffer.popleft()
                else:
                    self.audio_buffer[0] = buf[to_copy:]

            if not self.audio_buffer and filled < frames:
                self.drain_event.set()

    def play(self):
        if not self.playing:
            self.stream = sd.OutputStream(
                samplerate=self.sample_rate,
                channels=1,
                callback=self.callback,
                blocksize=self.buffer_size,
            )
            self.stream.start()
            self.playing = True
            self.drain_event.clear()

    def queue_audio(self, samples):
        self.drain_event.clear()

        with self.buffer_lock:
            self.audio_buffer.append(np.array(samples))
        if not self.playing:
            self.play()

    def wait_for_drain(self):
        return self.drain_event.wait()

    def stop(self):
        if self.playing:
            self.wait_for_drain()
            sd.sleep(100)

            self.stream.stop()
            self.stream.close()
            self.playing = False

    def flush(self):
        """Discard everything and stop playback immediately."""
        if not self.playing:
            return

        with self.buffer_lock:
            self.audio_buffer.clear()

        #  abort() is instantaneous; stop() waits for drain
        try:
            self.stream.abort()
        except AttributeError:  # older sounddevice
            self.stream.stop(ignore_errors=True)

        self.stream.stop()
        self.stream.close()
        self.playing = False
        self.drain_event.set()
