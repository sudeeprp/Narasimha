import unittest
from pillar_talk import PillarTalk
import story
from story import StoryState
from player import PlayerEvents
from doer import Doer

class ActuatorMock:
    def __init__(self):
        self.events_given_to_player = []
        self.events_given_to_serial = []
    def play(self, event, done):
        self.events_given_to_player.append(event)
        done() if done else None
    def serialtalk(self, event):
        self.events_given_to_serial.append(event)


class InteractionTest(unittest.TestCase):

    def test_nonsense_input_doesnt_crash(self):
        story.reset()
        replies = story.incoming('')
        self.assertEqual(len(replies), 0)
        self.assertEqual(story.state(), StoryState.booting)
        replies = story.incoming(None)
        self.assertEqual(len(replies), 0)

    def test_first_hit_after_boot_does_nothing(self):
        story.reset()
        replies = story.incoming('{"event": "CRACK"}')
        self.assertEqual(len(replies), 0)
        self.assertEqual(story.state(), StoryState.expect_hit)

    def test_first_hit_of_audience_gives_audio(self):
        story.set_state(StoryState.expect_hit)
        replies = story.incoming('{"event": "CRACK"}')
        self.assertEqual(len(replies), 1)
        self.assertEqual(replies[0]['do'], PlayerEvents.first_hit)
        self.assertIsNotNone(replies[0]['done'])
        actuator_mock = ActuatorMock()
        doer = Doer(actuator_mock.play, actuator_mock.serialtalk)
        doer.do(replies)
        self.assertEqual(actuator_mock.events_given_to_player[0], PlayerEvents.first_hit)
        self.assertEqual(story.state(), StoryState.expect_crack) # because the mock has called done()
        self.assertEqual(actuator_mock.events_given_to_serial[0], PlayerEvents.first_hit)

    def test_second_hit_of_audience_gives_audio_and_cracks_the_pillar(self):
        story.set_state(StoryState.expect_crack)
        actuator_mock = ActuatorMock()
        doer = Doer(actuator_mock.play, actuator_mock.serialtalk)
        doer.do(story.incoming('{"event": "CRACK"}'))
        self.assertEqual(actuator_mock.events_given_to_player[0], PlayerEvents.crack)
        self.assertEqual(story.state(), StoryState.expect_placement)
        self.assertEqual(actuator_mock.events_given_to_serial[1], PillarTalk.crack)

    def test_placement_triggers_fang_kick(self):
        story.set_state(StoryState.expect_placement)
        actuator_mock = ActuatorMock()
        doer = Doer(actuator_mock.play, actuator_mock.serialtalk)
        doer.do(story.incoming('{"hit":"H", "placed":"L"}'))
        self.assertEqual(actuator_mock.events_given_to_player[0], PlayerEvents.fang_kick)
        self.assertEqual(story.state(), StoryState.lakshmi_narasimha)
        self.assertEqual(actuator_mock.events_given_to_serial[1], PillarTalk.fang_kick)


if __name__ == '__main__':
    unittest.main()
