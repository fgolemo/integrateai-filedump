import json
import os

import matplotlib.pylab as plt
import numpy as np


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


class Tracker():
    def __init__(self, dir="flo", name="flo"):
        self.dir = dir
        self.name = name
        n_frames = len([filename for filename in os.listdir(self.dir) if 'pose' in filename])

        self.neck_x = np.zeros(n_frames)
        self.neck_y = np.zeros(n_frames)

        self.wrist_r_x = np.zeros(n_frames)
        self.wrist_r_y = np.zeros(n_frames)

        self.wrist_l_x = np.zeros(n_frames)
        self.wrist_l_y = np.zeros(n_frames)


        for i in np.arange(n_frames):
            filename = os.path.join(self.dir, self.name + '_%012d_pose.json' % int(i))
            pose = json.load(open(filename))
            body_parts = np.array(pose['people'][0]['body_parts'])
            self.neck_x[i] = body_parts[1 * 3]
            self.neck_y[i] = body_parts[1 * 3 + 1]
            self.wrist_r_x[i] = body_parts[4 * 3]
            self.wrist_r_y[i] = body_parts[4 * 3 + 1]
            self.wrist_l_x[i] = body_parts[7 * 3]
            self.wrist_l_y[i] = body_parts[7 * 3 + 1]

    def get_wrists_separate(self):
        return (
            self.neck_x,
            self.neck_y,
            self.wrist_r_x,
            self.wrist_r_y,
            self.wrist_l_x,
            self.wrist_l_y
        )

    def get_wrists(self):
        return np.stack(self.get_wrists_separate(), axis=0)

    def get_wrists_relative(self):
        # subtract neck from all wrists
        wrist_r_x_rel = self.wrist_r_x - self.neck_x
        wrist_r_y_rel = self.wrist_r_y - self.neck_y

        wrist_l_x_rel = self.wrist_l_x - self.neck_x
        wrist_l_y_rel = self.wrist_l_y - self.neck_y

        return np.stack((
            wrist_r_x_rel,
            wrist_r_y_rel,
            wrist_l_x_rel,
            wrist_l_y_rel
        ), axis=0)

if __name__ == '__main__':
    t = Tracker("../flo", "flo")
    print (t.get_wrists().shape)
