import sys
import tempfile
import unittest
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import storymode_adaptive_agent as agent

class AdaptiveAgentTests(unittest.TestCase):
    def make_image(self, state):
        im=Image.new("RGB",(1280,800),(10,20,25))
        d=ImageDraw.Draw(im)
        if state=="map":
            d.rectangle((100,40,1180,780),fill=(20,105,70))
            d.rectangle((400,180,900,680),fill=(20,105,70))
        elif state=="roulette":
            d.rectangle((100,70,700,730),fill=(180,15,25))
            d.rectangle((120,90,680,710),fill=(210,150,35))
        elif state=="dialogue":
            d.rectangle((130,515,1150,740),fill=(100,100,85))
            d.rectangle((130,515,1150,540),fill=(190,110,20))
            d.rectangle((200,580,800,600),fill=(245,245,245))
        elif state=="barrier_choice":
            d.rectangle((400,180,900,680),fill=(20,105,70))
            d.rectangle((920,550,1130,690),fill=(20,30,100))
            d.ellipse((935,560,1115,620),fill=(220,20,30))
            d.rectangle((590,395,685,460),fill=(20,100,230))
        return im
    def classify(self,state):
        with tempfile.NamedTemporaryFile(suffix=".png") as f:
            self.make_image(state).save(f.name)
            return agent.observe(f.name)
    def test_known_state_classes(self):
        for state in ("map","roulette","dialogue","barrier_choice"):
            with self.subTest(state=state):
                self.assertEqual(self.classify(state)["state"],state)
    def test_unknown_fails_closed(self):
        out=self.classify("unknown")
        self.assertEqual(out["state"],"unknown")
        self.assertEqual(out["action"],"WAIT")
    def test_dialogue_uses_start(self):
        self.assertEqual(self.classify("dialogue")["action"],"START")
    def test_yes_highlight_uses_contextual_circle(self):
        out=self.classify("barrier_choice")
        self.assertTrue(out["features"]["yes_selected_visual"])
        self.assertEqual(out["action"],"CIRCLE")
    def test_persistent_map_rotates_direction(self):
        with tempfile.TemporaryDirectory() as td:
            h=Path(td)/"history.json"
            h.write_text('{"last_state":"map","last_action":"DOWN","roulette_wait_count":0}')
            with tempfile.NamedTemporaryFile(suffix=".png") as f:
                self.make_image("map").save(f.name)
                self.assertEqual(agent.decide(f.name,h)["action"],"RIGHT")

if __name__=="__main__":
    unittest.main()
