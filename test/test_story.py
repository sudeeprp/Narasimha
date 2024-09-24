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

    def test_boot(self):
        story.reset()
        replies = story.incoming('{"event": "CRACK"}')
        self.assertEqual(len(replies), 0)
        self.assertEqual(story.state(), StoryState.expect_hit)

    def test_first_hit(self):
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

    def test_crack(self):
        story.set_state(StoryState.expect_crack)
        actuator_mock = ActuatorMock()
        doer = Doer(actuator_mock.play, actuator_mock.serialtalk)
        doer.do(story.incoming('{"event": "CRACK"}'))
        self.assertEqual(actuator_mock.events_given_to_player[0], PlayerEvents.crack)
        self.assertEqual(story.state(), StoryState.expect_placement)
        self.assertEqual(actuator_mock.events_given_to_serial[1], PillarTalk.crack)


if __name__ == '__main__':
    unittest.main()
