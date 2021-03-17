#!/usr/bin/python3
import sounddevice as sd
import matplotlib.pyplot as plt

def record(duration = None, fs = 44100, channels = 2):
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()
    return recording
def playback(recording, fs = 44100):
    sd.play(recording, fs)
    sd.wait()
def plot(recording):
    plt.plot(recording[0:1024])
    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    plt.title("Audio Sample")
    plt.show()


'''
def main():
    x = record(3)
    playback(x)
    plot(x)


if __name__ == '__main__':
    main()
'''
