from enum import Enum
import pygame
import time
import threading
import os

PlayerEvents = Enum('PlayerEvents', ['first_hit', 'crack', 'fang_kick_peace'])

audios = {
    PlayerEvents.first_hit: 'first_hit.mp3',
    PlayerEvents.crack: 'crack_for_narasimha.mp3',
    PlayerEvents.fang_kick_peace: 'fang_kick_peace.mp3'
}


def play_mp3(mp3_file, done):
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)

    def monitor_playback():
        print(f'playing {mp3_file}...')
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        print(f'...done playing {mp3_file}')
        done()

    pygame.mixer.music.play()
    threading.Thread(target=monitor_playback).start()


def play(event, done):
    if event in audios:
        play_mp3(os.path.join('audio', audios[event]), done)


if __name__ == '__main__':
    def print_done():
        print('done')
    play(PlayerEvents.first_hit, 
         lambda: play(PlayerEvents.crack, 
                      lambda: play(PlayerEvents.fang_kick_peace, print_done))
    )
