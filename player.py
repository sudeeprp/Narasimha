from enum import Enum
import pygame
import time
import threading
import os

PlayerEvents = Enum('PlayerEvents', ['first_hit', 'crack', 'fang', 'kick', 'sharanam', 'simha', 'peace'])

audios = {
    PlayerEvents.first_hit: 'first_hit.mp3',
    PlayerEvents.crack: 'crack_for_narasimha.mp3',
    PlayerEvents.fang: 'fang.mp3',
    PlayerEvents.kick: 'kick.mp3',
    PlayerEvents.sharanam: 'sharanam.mp3',
    PlayerEvents.simha: 'simha.mp3',
    PlayerEvents.peace: 'peace.mp3',
}

stop_requested = False


def stop_playing():
    global stop_requested
    stop_requested = True


def play_mp3(mp3_file, done):
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)

    def monitor_playback():
        print(f'playing {mp3_file}...')
        while pygame.mixer.music.get_busy():
            if stop_requested:
                pygame.mixer.music.stop()
                break
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
    # Testing the enum to filename mapping
    player_events = list(PlayerEvents)
    def play_event(event_index):
        play(player_events[event_index], lambda: play_event(event_index + 1))
    play_event(0)
