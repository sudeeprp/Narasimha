from enum import Enum
import json
from pillar_talk import PillarTalk

StoryState = Enum('StoryState', ['booting', 'expect_hit', 'first_hit', 'expect_crack', 'cracking',
                                 'expect_placement', 'fang_kick_peace'])

story_state = StoryState.booting


def parse_line(line):
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return None


def do_nothing(line): return []

def when_booting(line):
    if line == '{"event": "CRACK"}':
        set_state(StoryState.expect_hit)
    return []


def expect_first_hit(line):
    if line == '{"event": "CRACK"}':
        set_state(StoryState.first_hit)
        return [{'do': PillarTalk.first_hit, 'done': lambda: set_state(StoryState.expect_crack)}]
    return []


def expect_cracking(line):
    if line == '{"event": "CRACK"}':
        set_state(StoryState.cracking)
        return [{'do': PillarTalk.crack, 'done': lambda: set_state(StoryState.expect_placement)}]
    return []


def expect_placement(line):
    incoming_msg = parse_line(line)
    if incoming_msg and 'placed' in incoming_msg and incoming_msg['placed'] == 'L':
        set_state(StoryState.fang_kick_peace)
        return [{'do': PillarTalk.fang_kick_peace, 'done': lambda: set_state(StoryState.expect_hit)}]
    return []


storyline = {
    StoryState.booting: when_booting,
    StoryState.expect_hit: expect_first_hit,
    StoryState.first_hit: do_nothing,
    StoryState.expect_crack: expect_cracking,
    StoryState.cracking: do_nothing,
    StoryState.expect_placement: expect_placement,
    StoryState.fang_kick_peace: do_nothing
}


def set_state(s):
    global story_state
    story_state = s


def state():
    return story_state


def reset():
    set_state(StoryState.booting)


def incoming(line):
    if line:
        return storyline[story_state](line.strip())
    else:
        return []
