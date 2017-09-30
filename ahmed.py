import json 
import os
import numpy as np
import matplotlib.pylab as plt
import subprocess 

DIR = 'ahmed'

n_frames = len([filename for filename in os.listdir(DIR) if 'pose' in filename ])

RWrist_x_coord = np.zeros(n_frames)
RWrist_y_coord = np.zeros(n_frames)

LWrist_x_coord = np.zeros(n_frames)
LWrist_y_coord = np.zeros(n_frames)

for i in np.arange(n_frames):
	filename = os.path.join(DIR, 'ahmed_%012d_pose.json' % int(i))
	pose = json.load(open(filename))
	body_parts = np.array(pose['people'][0]['body_parts'])
	RWrist_x_coord[i] = body_parts[4 * 3]
	RWrist_y_coord[i] = body_parts[4 * 3 + 1]

	LWrist_x_coord[i] = body_parts[7 * 3]
	LWrist_y_coord[i] = body_parts[7 * 3 + 1]



f, ax = plt.subplots(2, 2)

ax[0, 0].plot(np.arange(n_frames), RWrist_x_coord)
ax[0, 1].plot(np.arange(n_frames), RWrist_y_coord)

ax[1, 0].plot(np.arange(n_frames), LWrist_x_coord)
ax[1, 1].plot(np.arange(n_frames), LWrist_y_coord)

plt.show()