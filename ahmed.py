import json 
import os
import numpy as np
import matplotlib.pylab as plt
from scipy.ndimage.filters import gaussian_filter
from scipy import signal
import pdb

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



# filtering 

RWrist_x_coord = gaussian_filter(RWrist_x_coord, 1)
RWrist_y_coord = gaussian_filter(RWrist_y_coord, 1)
LWrist_x_coord = gaussian_filter(LWrist_x_coord, 1)
LWrist_y_coord = gaussian_filter(LWrist_y_coord, 1)


# relative maximum retrieving
argrelmax_RWirst_y = signal.argrelmax(RWrist_y_coord, order=10)[0]
argrelmax_LWirst_y = signal.argrelmax(LWrist_y_coord, order=10)[0]

# 
# gradient_RWrist_x = np.gradient(RWrist_x_coord, 2)
# gradient_LWrist_x = np.gradient(LWrist_x_coord, 2)
def which_dump(x):
	if x <= 350:
		return 1
	elif (x > 350) and (x <= 500):
		return 2 
	elif (x > 500) and (x <= 600):
		return 3
	else:
 		return 4


key_points = []
for idx in argrelmax_RWirst_y:
	key_points.append([idx, RWrist_x_coord[idx], RWrist_y_coord[idx], 
		which_dump(RWrist_x_coord[idx])])

for idx in argrelmax_LWirst_y:
	key_points.append([idx, LWrist_x_coord[idx], LWrist_y_coord[idx], 
		which_dump(LWrist_x_coord[idx])])


np.save('ahmed_key_points.npy', np.array(key_points))
# pdb.set_trace()

# f, ax = plt.subplots(2, 3)

# # n_frames = RWrist_x_coord

# ax[0, 0].plot(np.arange(n_frames), RWrist_x_coord)
# ax[0, 1].plot(np.arange(n_frames), RWrist_y_coord)
# ax[0, 1].plot(argrelmax_RWirst_y, RWrist_y_coord[argrelmax_RWirst_y], 'o')
# ax[0, 0].plot(argrelmax_RWirst_y, RWrist_x_coord[argrelmax_RWirst_y], 'o')

# # ax[0, 2].plot(np.arange(n_frames), gradient_RWrist_x)

# ax[1, 0].plot(np.arange(n_frames), LWrist_x_coord)
# ax[1, 1].plot(np.arange(n_frames), LWrist_y_coord)
# ax[1, 0].plot(argrelmax_LWirst_y, LWrist_x_coord[argrelmax_LWirst_y], 'o')
# ax[1, 1].plot(argrelmax_LWirst_y, LWrist_y_coord[argrelmax_LWirst_y], 'o')

# # ax[1, 2].plot(np.arange(n_frames), gradient_LWrist_x)


# plt.show()