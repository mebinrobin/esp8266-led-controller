import pyaudio


class Microphone:
    def __init__(self, mic_rate: int = 44100, refresh_rate: int = 60):
        self._ai = pyaudio.PyAudio()
        self._buffer_size = int(mic_rate/refresh_rate)
        self._stream = self._ai.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=mic_rate,
            input_device_index=0,
            input=True,
            frames_per_buffer=self._buffer_size,
            start=False,
        )

    def __enter__(self):
        return self, self._stream

    def start(self):
        self._stream.start_stream()

    def stop(self):
        self._stream.stop_stream()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stream.stop_stream()
        self._stream.close()
        self._ai.terminate()
