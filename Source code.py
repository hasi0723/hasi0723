
# Import necessary libraries
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import time

# Constants
CHUNK = 2048  # samples per frame
FORMAT = pyaudio.paInt16  # audio format (bytes per sample?)
CHANNELS = 1  # single channel for microphone
RATE = 44100  # samples per second

# Create matplotlib figure and axes
fig, ax = plt.subplots(1, figsize=(15, 7))

# PyAudio class instance
p = pyaudio.PyAudio()

# Get list of available inputs
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

# Print available input devices
for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

# Select input audio device
audio_input = input("\n\nSelect input by Device id: ")

# Stream object to get data from microphone
stream = p.open(
    input_device_index=int(audio_input),
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

# Variable for plotting
x = np.arange(0, 2 * CHUNK, 2)

# Create a line object with random data
line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)

# Basic formatting for the axes
ax.set_title('AUDIO WAVEFORM')
ax.set_xlabel('samples')
ax.set_ylabel('volume')
ax.set_ylim(0, 255)
ax.set_xlim(0, 2 * CHUNK)
plt.setp(ax, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])

# Show the plot
plt.show(block=False)
print('stream started')

# For measuring frame rate
frame_count = 0
start_time = time.time()

while True:
    # Binary data
    data = stream.read(CHUNK)

    # Convert data to integers, make np array, then offset it by 127
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
    data_np = np.array(data_int, dtype='b')[::2] + 128

    # Update line data
    line.set_ydata(data_np)

    # Update figure canvas
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        frame_count += 1
    except TclError:
        # Calculate average frame rate
        frame_rate = frame_count / (time.time() - start_time)
        print('stream stopped')
        print('average frame rate = {:.0f} FPS'.format(frame_rate))
        break
```
This code is a real-time audio visualizer that uses PyAudio to stream audio data from a microphone and Matplotlib to display the waveform. The code has been reorganized for better readability, with added comments to explain each section.
