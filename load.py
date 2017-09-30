import json 
import os
import numpy as np
import matplotlib.pylab as plt
import subprocess 


# plt.gca().invert_xaxis()
# plt.gca().invert_yaxis()

DIR = 'output3'

n_frames = len([filename for filename in os.listdir(DIR) if 'pose' in filename ])
# POSE_COCO_BODY_PARTS = [
#         {0,  "Nose"},
#         {1,  "Neck"},
#         {2,  "RShoulder"},
#         {3,  "RElbow"},
#         {4,  "RWrist"},
#         {5,  "LShoulder"},
#         {6,  "LElbow"},
#         {7,  "LWrist"},
#         {8,  "RHip"},
#         {9,  "RKnee"},
#         {10, "RAnkle"},
#         {11, "LHip"},
#         {12, "LKnee"},
#         {13, "LAnkle"},
#         {14, "REye"},
#         {15, "LEye"},
#         {16, "REar"},
#         {17, "LEar"},
#         {18, "Bkg"}
#     ]
x_indices = [3*int(i) for i in np.arange(18)]
y_indices = [3*int(i) + 1 for i in np.arange(18)]

RWrist_x_coord = np.zeros(n_frames)
RWrist_y_coord = np.zeros(n_frames)

for i in np.arange(n_frames):
	filename = os.path.join(DIR, 'test3_%012d_pose.json' % int(i))
	pose = json.load(open(filename))
	body_parts = np.array(pose['people'][0]['body_parts'])
	RWrist_x_coord[i] = body_parts[4 * 3]
	RWrist_y_coord[i] = body_parts[4 * 3 + 1]
	# x_coordinates = body_parts[x_indices]
	# y_coordinates = body_parts[y_indices]

f, (ax1, ax2) = plt.subplots(1, 2)

ax1.plot(np.arange(n_frames), RWrist_x_coord)
ax2.plot(np.arange(n_frames), RWrist_y_coord)

plt.show()

