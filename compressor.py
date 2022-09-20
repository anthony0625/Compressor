import numpy as np
import pyaudio
import time
import sys


class Compressor:
    def __init__(self, upper_threshold, upper_ratio, upper_knee=0, lower_threshold=0, lower_ratio=1, lower_knee=0):
        #Parameters
        self.upper_threshold = upper_threshold
        self.upper_ratio = upper_ratio
        self.upper_knee = upper_knee
        self.lower_threshold = lower_threshold
        self.lower_ratio = lower_ratio
        self.lower_knee = lower_knee
        
        self.vcompress = np.vectorize(self.compress)
        
        #Stream setup
        self.pyaudioinstance = pyaudio.PyAudio()
        self.stream = self.pyaudioinstance.open(format=pyaudio.paFloat32,
                                                channels = 1,
                                                rate = 44100,
                                                input = True,
                                                output = True,
                                                frames_per_buffer = 1024,
                                                stream_callback = self.callback)
        self.stream.start_stream()
        while self.stream.is_active():
            time.sleep(1)#0.2
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudioinstance.terminate()
        sys.exit()
    
    def callback(self, in_data, frame_count, time_info, status):
       in_data = np.frombuffer(in_data, dtype=np.float32)
       in_data = self.vcompress(in_data)
       print(in_data.max())
       print(in_data.min())
       return (in_data, pyaudio.paContinue)
   
    def compress(self, signal):
        if signal>self.upper_threshold:
            return self.upper_threshold + (signal - self.upper_threshold) * self.upper_ratio
        elif signal<self.lower_threshold:
            return self.lower_threshold - (signal + self.lower_threshold) * self.lower_ratio
        else:
            return signal
        
temp = Compressor(1,1)