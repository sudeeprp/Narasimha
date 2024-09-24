from enum import Enum
import pygame
import time
import threading
import os

def play_mp3(mp3_file, done):
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)

    def monitor_playback():
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        done()

    pygame.mixer.music.play()
    threading.Thread(target=monitor_playback).start()


PlayerEvents = Enum('PlayerEvents', ['first_hit', 'crack'])


audios = {
    PlayerEvents.first_hit: 'first_hit.mp3'
}


def play(event, done):
    if event in audios:
        play_mp3(os.path.join('audio', audios[event]), done)


if __name__ == '__main__':
    def print_done():
        print('done')
    play(PlayerEvents.first_hit, print_done)
