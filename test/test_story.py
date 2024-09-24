import unittest
import story
from story import StoryState

class InteractionTest(unittest.TestCase):

    def test_boot(self):
        story.reset()
        replies = story.incoming('{"event": "CRACK"}')
        self.assertEqual(len(replies), 0)
        self.assertEqual(story.state(), StoryState.wait_for_hit)

    def test_crack(self):
        story.set_state(StoryState.wait_for_hit)
        replies = story.incoming('{"event": "CRACK"}')
        self.assertEqual(len(replies), 1)


if __name__ == '__main__':
    unittest.main()
