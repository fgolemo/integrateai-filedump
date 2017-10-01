import numpy as np
import pygame
from pygame.locals import*
import imageio
import cv2
from scikits.samplerate import resample
from tqdm import tqdm

DIR = "./gabo3" # directory
VIDEO_FPS = 30 # how many FPS was teh initial video recorded with
NUMBER_OF_NOTES = 20 # so many different sound pitches exist
# LATENCY_COMPENSATION = 8 # how much earlier does the audio play, USE WHEN RECORDING
LATENCY_COMPENSATION = 0 # how much earlier does the audio play, USE WHEN VIEWING/DEMOING
# LATENCY_COMPENSATION = -4 # how much later does the audio play, USE WHEN YOUTUBE




# PLEASE FIRST INSTALL scikits.samplerate
#
# sudo apt-get install libsamplerate0-dev
# sudo pip3 install git+https://github.com/gregorias/samplerate.git





data = np.load("{}/out.npz".format(DIR))["data"]

reader = imageio.get_reader('{}/result.avi'.format(DIR))
# writer = imageio.get_writer('{}/testing.mp4'.format(DIR))

white = (255, 64, 64)

init = False

clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 2, 512)  # smaller buffer
pygame.mixer.init()
pygame.mixer.set_num_channels(32)


# sound_file = "samples/pfff.wav"
sound_file = "samples/powerchord2.wav"
sound = pygame.mixer.Sound(sound_file)

# load the sound into an array
snd_array = pygame.sndarray.array(sound)

sounds = []

for i in range(NUMBER_OF_NOTES):

    # pitch_scaling = .1 + (2.0 * i / NUMBER_OF_NOTES) # this is unrealistic, but gives you more pitch spread
    pitch_scaling = .4 + (.8 * i / NUMBER_OF_NOTES) # this is somewhat realistic for one string

    # resample. args: (target array, ratio, mode), outputs ratio * target array.
    snd_resample = resample(snd_array, pitch_scaling, "sinc_fastest").astype(snd_array.dtype)

    #make the sounds into a pygame obj again
    snd_out = pygame.sndarray.make_sound(snd_resample)

    sounds.append(snd_out)

# invert sounds list (low index = low sound, high index = high sound)
# sounds = sounds[::-1] # nope, actually not the case... :)

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
        note = int(round(data[data[:,0] == idx+LATENCY_COMPENSATION][0,1] * NUMBER_OF_NOTES))
        print("\nplaying note: {}".format(note))
        sounds[note-1].play()

    clock.tick(VIDEO_FPS) # enforce framerate




