# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# clear memory
import gc

from time import sleep
from math import ceil
from random import randint
from usb_midi import ports

from simpleio import map_range

from adafruit_midi import MIDI
from adafruit_midi.note_on import NoteOn
from adafruit_circuitplayground import cp
from adafruit_circuitplayground.express import cpx

gc.collect()
cp.pixels.brightness = 0.2

midi = MIDI(midi_out=ports[1], out_channel=0)

velocity = 127

# READ IN PITCH
pitch_readings = [90] * 4  # number of readings

# Booleans
set_neutral = True
in_loop = True

def getPitch(pitch_readings):
    x, y, z = cpx.acceleration

    pitch_readings = pitch_readings[1:]
    pitch_readings.append(map_range(y, -9.8, 9.8, 0, 180))
    currPitch = sum(pitch_readings) / len(pitch_readings)

    return currPitch, pitch_readings

def light():
    c = 255
    cp.pixels.fill((randint(1, c), randint(1, c), randint(1, c)))

while True:
    pitch, pitch_readings = getPitch(pitch_readings)

    # TILT READING WITH THUMB PRESS
    # correlates to rewind/forward
    if (cp.touch_A6):
        print(pitch)
        if (pitch <= 80):                           # convert 0-80 to 0-30 scale
            pitch = pitch * 3/8
        elif (pitch <= 100):                        # convert 80-100 to 30-90 scale
            pitch = (pitch-80) * 3 + 30
        else:                                       # convert 100-180 to 90-120 scale
            pitch = (pitch-100) * 3/8 + 90
        print(pitch)
        midi.send(NoteOn(ceil(pitch), velocity))

        # flash light
        light()

        # set booleans
        set_neutral = True
        in_loop = False
    # TILT READING WITH INDEX PRESS
    # correlates to finetuning speed of normal play
    elif (cp.touch_TX):
        print(pitch)
        pitch = pitch * 1/6 + 15                   # convert 0-180 to 15-45 scale
        print(pitch)
        midi.send(NoteOn(ceil(pitch), velocity))

        # flash light
        light()

        # set booleans
        set_neutral = True
        in_loop = False
    # MIDDLE
    elif (cp.touch_A1):
        midi.send(NoteOn(122, velocity))

        # flash light
        light()

        # set booleans
        set_neutral = True
        in_loop = False
    # RING
    # set loop
    elif (cp.touch_A2):
        if (in_loop):
            midi.send(NoteOn(124, velocity))
        else:
            midi.send(NoteOn(123, velocity))
            in_loop = True

        # flash light
        light()

        # set boolean
        set_neutral = True
    # PINKY
    elif (cp.touch_A3):
        midi.send(NoteOn(125, velocity))

        # flash light
        light()

        # set booleans
        in_loop = False
        set_neutral = True
    elif (set_neutral):
        midi.send(NoteOn(126, velocity))

        # set booleans
        in_loop = False
        set_neutral = False
    else:
        # turn off light
        cp.pixels.fill((0, 0, 0))

    sleep(0.1)
