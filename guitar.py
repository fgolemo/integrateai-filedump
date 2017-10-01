import matplotlib.pyplot as plt
import numpy as np

from tracker.tracker import Tracker

DIR = "./flo" # directory
NAME = "flo" # prefix of json files
FRAMES_AFTER_PEAK = 3 # what's the minimal distance from the strumming that a peak can occur - bigger = more strums removed
DELAY_AFTER_ACTIVATION = 5 # how many steps after a frame is it impossible to strum again
FRAME_INTERPOLATION_SCALE = 3  # higher = more interpol, UNUSED
MIN_DIFFERENCE = 15 # what's the minimum pixel movement required in the last FRAMES_AFTER_PEAK frames to trigger strum

NOTE_SHIFT = +2 # where is the left hand note grabbed (negative = earlier in time)

MAX_WRIST_NECK_DIST = 230 # max length between left wrist and neck in pixels, should be calibrated beforehand in live env

t = Tracker(DIR, NAME)

# relative vis
data = t.get_wrists()
n_frames = data.shape[1]

left_hand_distances = np.sqrt(np.power(data[0, :] - data[4, :], 2) + np.power(data[1, :] - data[5, :], 2))

# normalize
left_hand_distances /= MAX_WRIST_NECK_DIST

# _, (ax1, ax2) = plt.subplots(2, 1)
_, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

x = np.arange(n_frames)

n_frames_smol = int(n_frames / FRAME_INTERPOLATION_SCALE)

ax1.plot(x, left_hand_distances, label="notes", c="black")

ax2.plot(x, data[3, :], label="strumming", c="black")
strumming_d1 = np.gradient(data[3, :])
strumming_d2 = np.gradient(strumming_d1)
ax4.plot(x, strumming_d1, c="red")
# ax4.plot(x, strumming_d2, c="blue")

extrema = []

# find all downward strums
for i in range(n_frames - 1):
    if i > FRAMES_AFTER_PEAK:
        if (strumming_d2[i] > 0 and strumming_d2[i + 1] < 0):
            extrema.append(i + 1)

extrema_filtered = []

# filter extrema to remove small strums
for e in extrema:
    keep = True

    if data[3, e] - data[3, e - FRAMES_AFTER_PEAK + 1] < MIN_DIFFERENCE:
        keep = False

    # if keep:
    #     for j in range(FRAMES_AFTER_PEAK - 1):
    #         if data[3, e - j - 1] < data[3, e - j]:
    #             keep = False
    #             break

    if keep:
        if len(extrema_filtered) == 0 or extrema_filtered[-1] < e - DELAY_AFTER_ACTIVATION:
            extrema_filtered.append(e)

# this variable stores the results
out = []

print ("frame, note to play [0,1] (1 = low, 0 = high)")

for e in extrema_filtered:
    ax2.axvline(x=e)
    ax4.axvline(x=e)
    ax1.axvline(x=e+NOTE_SHIFT)

    out_buffer = (e, left_hand_distances[e+NOTE_SHIFT])
    print (out_buffer)
    out.append(out_buffer)

for axis in [ax1, ax2]:
    axis.legend()
plt.show()

out_matrix = np.array(out)

# RESULTS are stored in variable: out and out_matrix

import imageio
import cv2
from tqdm import tqdm
boxsize = 20
reader = imageio.get_reader('{}/result.avi'.format(DIR))
writer = imageio.get_writer('{}/impacts.mp4'.format(DIR))

for idx, im in tqdm(enumerate(reader)):
    if idx in out_matrix[:,0]:
        # plot impact
        x1, y1, x2, y2 = 0, 0, 200, 200

        cv2.rectangle(im, (x1, y1), (x2, y2), (255, 0, 0), -1)

    writer.append_data(im)
writer.close()