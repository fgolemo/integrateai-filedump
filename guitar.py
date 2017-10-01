from tracker.tracker import Tracker
import matplotlib.pyplot as plt
import numpy as np

DIR="./flo"
NAME="flo"
FRAMES_AFTER_PEAK = 3
DELAY_AFTER_ACTIVATION = 10


t = Tracker(DIR, NAME)

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

# TODO: write code for guitar
