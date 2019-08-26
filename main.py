# from openbci import ganglion as bci
# print(dir(bci))

from time import sleep, time
from threading import Thread

import numpy as np
import matplotlib.pyplot as plt

from pyOpenBCI import OpenBCIGanglion

VOLTS_PER_COUNT = 1.2 * 8388607.0 * 1.5 * 51.0
SAMPLE_POINTS = 200

# TODO: Move to class
timings = []
samples = []


def reader(sample):
    #print(sample)
    volts = sample.channels_data / VOLTS_PER_COUNT
    timings.append(time())
    samples.append(volts[0])
    #print(volts)
    #print(len(data))


def plot():
    if len(timings) > SAMPLE_POINTS:
        plt.axis([0, 200, -0.01, 0.01])
        s = np.array(samples)
        #print(s)
        #print(s.shape)
        s = s[-SAMPLE_POINTS:]
        sp = np.fft.fft(s, axis=0)
        timestep = timings[-1] - timings[-2]   # should be ~200Hz
        print(timestep)
        freq = np.fft.fftfreq(s.shape[0], timestep)
        i = freq > 0  # get positive half of frequencies
        #print(timings)
        plt.plot(freq[i], sp.real[i])
        plt.pause(0.01)
        plt.cla()  # clear axes
        #plt.show()
        #print('pltd')


def main():
    print("Connecting...")
    board = OpenBCIGanglion(mac='ff:ce:cf:9f:7d:74')
    print("Connected!")
    t = Thread(target=board.start_stream, args=(reader,), daemon=True)
    t.start()

    while True:
        plot()
        sleep(0.01)


if __name__ == "__main__":
    main()
