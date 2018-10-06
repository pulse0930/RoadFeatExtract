#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Horn detection Get Instensities per second
from scipy.io import wavfile as wav
import numpy as np
import scipy
from progress import printProgressBar
import os
import sys

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def convert_to_hhmmss(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h,24)
    return "%02d:%02d:%02d" % (h, m, s)

def date_time(text,i):
    import re
    var = re.findall(r'\d+',text.split('/')[-1])
    seconds = get_sec(var[3]+':'+var[4]+':'+var[5]) + i
    return var[1]+'/'+var[2]+'/'+var[0]+' '+convert_to_hhmmss(seconds)

def convert_to_mono(x):
    return x.astype(float).sum(axis=1) / 2

def band_pass(x,sr,fL,fU):
    x = list(np.array(x))
    i = 1
    out = []
    while i*sr<len(x):
        x_ = x[(i-1)*sr:i*sr]
        fft_out = np.fft.fft(x_)
        fft_out[0:fL] = 0
        fft_out[fU:-1] = 0
        wave = np.fft.ifft(fft_out)
        out += list(wave.real)
        i += 1
    return np.array(out).astype(np.int16)

def write_audio(x,sr,filename = 'work.wav'):
    scipy.io.wavfile.write(filename,sr,x)

def read_audio(filename):
    sr, x = wav.read(filename)
    return sr,x

def dbfft(x, fs, win=None, ref=32768):
    """
    Calculate spectrum in dB scale
    Args:
        x: input signal
        fs: sampling frequency
        win: vector containing window samples (same length as x).
             If not provided, then rectangular window is used by default.
        ref: reference value used for dBFS scale. 32768 for int16 and 1 for float

    Returns:
        freq: frequency vector
        s_db: spectrum in dB scale
    """

    N = len(x)  # Length of input sequence

    if win is None:
        win = np.ones(N)
    if len(x) != len(win):
            raise ValueError('Signal and window must be of the same length')
    x = x * win

    # Calculate real FFT and frequency vector
    sp = np.fft.rfft(x)
    freq = np.arange((N / 2) + 1) / (float(N) / fs)

    # Scale the magnitude of FFT by window and factor of 2,
    # because we are using half of FFT spectrum.
    s_mag = np.abs(sp) * 2 / np.sum(win)

    # Convert to dBFS
    s_dbfs = 20 * np.log10(s_mag/ref)

    # Scale from dBFS to dB
    K = 120
    s_db = s_dbfs + K
    return freq, s_db

# def plot_freqAmpDb(freq,s_db,i):
#     print('Time:',i,'sec')
#     print('Max amplitude:',np.max(s_db),'db')
#     print('Frequency:',freq[np.argmax(s_db)],'hz')
#     plt.plot(freq,s_db)
#     plt.grid(True)
#     plt.xlabel('Frequency [Hz]')
#     plt.ylabel('Amplitude [dB]')
#     plt.show()
#     plt.grid(True)

def main():
    filename = sys.argv[1]
    folder = sys.argv[2]
    sr, x = read_audio(filename)
    # print(x.shape)
    if len(x.shape) == 2: # if channael is stereo then convert it to mono
           x = convert_to_mono(x)
    X = band_pass(x, sr, 2000, 5001)
    i = 1
    pwd = os.getcwd()
    os.chdir(folder)
    f= open("processed_"+os.path.basename(filename)[:-4]+".txt","w+")
    while i*sr<len(X):
       x_ = X[(i-1)*sr:i*sr]
       # Take slice
       N = 8000
       win = np.hamming(N)
       freq, s_db = dbfft(x_, sr, win)
       f.write( date_time(filename,i)+','+str(np.max(s_db))+'\n')
       i += 1
       printProgressBar(i*sr,len(X))
    f.close()
    write_audio(X,sr,os.path.basename(filename)[:-4]+'_filtered.wav')
    os.chdir(pwd)

if __name__== "__main__":
  main()
