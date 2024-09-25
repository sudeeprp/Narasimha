import unittest
from pillar_talk import PillarTalk
import story
from story import StoryState
from doer import Doer

class ActuatorMock:
    def __init__(self):
        self.events_requested = []
    def request(self, event, done):
        self.events_requested.append(event)
        done() if done else None


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
        self.assertEqual(replies[0]['do'], PillarTalk.first_hit)
        self.assertIsNotNone(replies[0]['done'])
        actuator_mock = ActuatorMock()
        doer = Doer(actuator_mock.request)
        doer.do(replies)
        self.assertEqual(actuator_mock.events_requested[0], PillarTalk.first_hit)
        self.assertEqual(story.state(), StoryState.expect_crack) # because the mock has called done()

    def test_second_hit_of_audience_gives_audio_and_cracks_the_pillar(self):
        story.set_state(StoryState.expect_crack)
        actuator_mock = ActuatorMock()
        doer = Doer(actuator_mock.request)
        doer.do(story.incoming('{"event": "CRACK"}'))
        self.assertEqual(actuator_mock.events_requested[0], PillarTalk.crack)
        self.assertEqual(story.state(), StoryState.expect_placement)

    def test_placement_triggers_fang_kick_peace(self):
        story.set_state(StoryState.expect_placement)
        actuator_mock = ActuatorMock()
        doer = Doer(actuator_mock.request)
        doer.do(story.incoming('{"hit":"H", "placed":"L"}'))
        self.assertEqual(actuator_mock.events_requested[0], PillarTalk.fang_kick_peace)
        self.assertEqual(story.state(), StoryState.expect_hit)


if __name__ == '__main__':
    unittest.main()
