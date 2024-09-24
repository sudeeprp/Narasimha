from enum import Enum
from player import Player

StoryState = Enum('StoryState', ['booting', 'wait_for_hit', 'first_hit', 'wait_for_crack'])

story_state = StoryState.booting


def when_booting(line):
    if line == '{"event": "CRACK"}':
        set_state(StoryState.wait_for_hit)
    return []


def before_first_hit(line):
    if line == '{"event": "CRACK"}':
        set_state(StoryState.first_hit)
    return [Player.first_hit]


storyline = {
    StoryState.booting: when_booting,
    StoryState.wait_for_hit: before_first_hit
}


def set_state(s):
    global story_state
    story_state = s


def state():
    return story_state


def reset():
    set_state(StoryState.booting)


def incoming(line):
    return storyline[story_state](line)
