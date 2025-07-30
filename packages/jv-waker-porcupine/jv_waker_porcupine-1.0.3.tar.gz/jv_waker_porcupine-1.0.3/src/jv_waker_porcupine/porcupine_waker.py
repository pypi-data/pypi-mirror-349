import pvporcupine
import pyaudio
from struct import unpack
from jvcore import Waker, getConfig

class PorcupineWaker(Waker):
    def __init__(self) -> None:
        self._config = getConfig().get('waker.porcupine')
        self._keywords = self._config['wakewords']
        self._porcupine = pvporcupine.create(
            access_key= self._config['accessKey'],
            keywords=self._keywords
        )
        self._pyaudio = pyaudio.PyAudio() 
        self._stream = self._pyaudio.open(format=pyaudio.paInt16,
                channels=1,
                rate=self._porcupine.sample_rate,
                frames_per_buffer=self._porcupine.frame_length,
                input=True)
        
    def wakeword_detected(self) -> str:        
        result = self._porcupine.process(self.read_sample())
        return self._keywords[result] if result >=0 else None

    def __del__(self):
        self._porcupine.delete() if self._porcupine else None

        self._stream.stop_stream() if self._stream else None
        self._stream.close() if self._stream else None
        self._pyaudio.terminate() if self._pyaudio else None
        
    def read_sample(self):
        bytes = self._stream.read(self._porcupine.frame_length)
        return unpack(f'{len(bytes)//2}H',bytes) # unpacking to convert bytes to list of shorts (2ByteInts)


#default_input_device_index = p.get_default_input_device_info()
        
# p = pyaudio.PyAudio()
# info = p.get_host_api_info_by_index(0)
# numdevices = info.get('deviceCount')
# print('kjlkjl')
# for i in range(0, numdevices):
#     if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
#         print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))