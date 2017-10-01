import numpy as np
import pygame
from pygame.locals import*
import imageio
import cv2
# from scikits.samplerate import resample
from tqdm import tqdm
import os
import pdb

DIR = "./ahmed" # directory
VIDEO_FPS = 30 # how many FPS was teh initial video recorded with
NUMBER_OF_NOTES = 20 # so many different sound pitches exist
# LATENCY_COMPENSATION = 8 # how much earlier does the audio play, USE WHEN RECORDING
LATENCY_COMPENSATION = 0 # how much earlier does the audio play, USE WHEN VIEWING/DEMOING




# PLEASE FIRST INSTALL scikits.samplerate
#
# sudo apt-get install libsamplerate0-dev
# sudo pip3 install git+https://github.com/gregorias/samplerate.git





data = np.load("{}/out.npy".format(DIR))


reader = imageio.get_reader('{}/result.avi'.format(DIR))
# writer = imageio.get_writer('{}/testing.mp4'.format(DIR))

white = (255, 64, 64)

init = False

clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 2, 512)  # smaller buffer
pygame.mixer.init()
pygame.mixer.set_num_channels(32)

sound_dir = "./drum-samples"
sounds = list()
for sound_file in os.listdir(sound_dir):
    # pdb.set_trace()
    sounds.append(pygame.mixer.Sound(os.path.join(sound_dir, sound_file)))


print ("sound test")

def make_array_to_pygame_img(array):
    return pygame.surfarray.make_surface(array.transpose(1,0,2))

for idx, im in tqdm(enumerate(reader)):
    if not init:
        w = im.shape[1]
        h = im.shape[0]
        screen = pygame.display.set_mode((w, h))
        screen.fill((white))
        init = True

    screen.fill((white))
    surf = make_array_to_pygame_img(im)
    screen.blit(surf, (0, 0))
    pygame.display.flip()

    if idx+LATENCY_COMPENSATION in data[:,0]:
        # plot impact
        note = int(data[ data[:, 0] == idx+LATENCY_COMPENSATION][0,-1])
        print("\nplaying note: {}".format(note))
        sounds[note-1].play()

    clock.tick(VIDEO_FPS) # enforce framerate




