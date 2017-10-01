from tracker.tracker import Tracker
import matplotlib.pyplot as plt
import numpy as np

DIR="./flo"
NAME="flo"
FRAMES_AFTER_PEAK = 3
DELAY_AFTER_ACTIVATION = 10


t = Tracker(DIR, NAME)

# absolute visualization
data = t.get_wrists_relative()
n_frames = data.shape[1]

_, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

ax1.plot(np.arange(n_frames), data[0], label="right arm x")
ax2.plot(np.arange(n_frames), data[1], label="right arm y")

ax3.plot(np.arange(n_frames), data[2], label="left arm x")
ax4.plot(np.arange(n_frames), data[3], label="left arm y")

for axis in [ax1, ax2, ax3, ax4]:
    axis.legend()
plt.show()

# relative vis
data = t.get_wrists()
n_frames = data.shape[1]

left_hand_distances = np.sqrt(np.power(data[0,:]-data[4,:], 2) + np.power(data[1,:]-data[5,:], 2))

_, (ax1, ax2) = plt.subplots(2, 1)

ax1.plot(np.arange(n_frames), left_hand_distances, label="notes")
ax2.plot(np.arange(n_frames), data[3, :], label="strumming")

for axis in [ax1, ax2]:
    axis.legend()
plt.show()
