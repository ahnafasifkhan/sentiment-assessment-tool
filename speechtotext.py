# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 15:04:06 2020

@author: DELL
"""


import pyaudio
import wave
from google.cloud import speech
import io


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 20
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

client = speech.SpeechClient()

# path = 'resources/commercial_mono.wav'
with io.open('output.wav', 'rb') as audio_file:
    content = audio_file.read()

audio = speech.types.RecognitionAudio(content=content)
config = speech.types.RecognitionConfig(
    encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=8000,
    language_code='en-US',
    # Enable automatic punctuation
    enable_automatic_punctuation=True)

response = client.recognize(config, audio)

for i, result in enumerate(response.results):
    alternative = result.alternatives[0]
    print('-' * 20)
    print('First alternative of result {}'.format(i))
    print('Transcript: {}'.format(alternative.transcript))