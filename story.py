from enum import Enum
from player import PlayerEvents
from pillar_talk import PillarTalk

StoryState = Enum('StoryState', ['booting', 'expect_hit', 'first_hit', 'expect_crack', 'cracking',
                                 'expect_placement'])

story_state = StoryState.booting


def do_nothing(line): pass

def when_booting(line):
    if line == '{"event": "CRACK"}':
        set_state(StoryState.expect_hit)
    return []


def expect_first_hit(line):
    if line == '{"event": "CRACK"}':
        set_state(StoryState.first_hit)
        return [{'do': PlayerEvents.first_hit, 'done': lambda: set_state(StoryState.expect_crack)}]
    return []


def expect_cracking(line):
    if line == '{"event": "CRACK"}':
        set_state(StoryState.cracking)
        return [{'do': PlayerEvents.crack, 'done': lambda: set_state(StoryState.expect_placement)},
                {'do': PillarTalk.crack}]


storyline = {
    StoryState.booting: when_booting,
    StoryState.expect_hit: expect_first_hit,
    StoryState.first_hit: do_nothing,
    StoryState.expect_crack: expect_cracking,
    StoryState.expect_placement: do_nothing # TODO: replace with function to process placement
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
