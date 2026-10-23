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
        elif state=="sparse_dialogue":
            # Authentic C01-F100 has a visible gold dialogue box before
            # readable white Japanese glyphs appear; use START, never Circle.
            d.rectangle((130,515,1150,740),fill=(30,45,40))
            d.rectangle((130,515,1150,540),fill=(190,110,20))
            d.rectangle((130,715,1150,740),fill=(190,110,20))
            d.rectangle((130,540,155,715),fill=(190,110,20))
            d.rectangle((1125,540,1150,715),fill=(190,110,20))
        elif state in ("card_selection","card_selection_with_dialogue"):
            d.rectangle((100,40,1180,780),fill=(20,105,70))
            d.rectangle((400,180,900,680),fill=(20,105,70))
            # Mimic the authentic three-card overlay: pale frames and low-chroma patterned backs.
            for rect in ((390,230,590,520),(585,230,760,520),(750,230,900,520)):
                d.rectangle(rect,fill=(70,80,80),outline=(245,245,245),width=12)
                x1,y1,x2,y2=rect
                d.line((x1+18,y1+40,x2-18,y2-40),fill=(200,200,200),width=5)
                d.line((x1+18,y2-40,x2-18,y1+40),fill=(200,200,200),width=5)
            if state=="card_selection_with_dialogue":
                # The authentic card chooser overlays the same bottom box that normally
                # signals dialogue, so the specific card signature must win classifier priority.
                d.rectangle((130,515,1150,740),fill=(100,100,85))
                d.rectangle((130,515,1150,540),fill=(190,110,20))
                d.rectangle((130,715,1150,740),fill=(190,110,20))
                d.rectangle((130,540,155,715),fill=(190,110,20))
                d.rectangle((1125,540,1150,715),fill=(190,110,20))
        elif state=="barrier_choice":
            d.rectangle((400,180,900,680),fill=(20,105,70))
            d.rectangle((920,550,1130,690),fill=(20,30,100))
            d.ellipse((935,560,1115,620),fill=(220,20,30))
            d.rectangle((590,395,685,460),fill=(20,100,230))
        elif state=="map_after_move":
            d.rectangle((100,40,1180,780),fill=(20,105,70))
            d.rectangle((400,180,900,680),fill=(20,105,70))
            d.rectangle((430,50,650,190),fill=(190,20,20))
            d.rectangle((650,50,900,190),fill=(15,60,210))
            d.rectangle((500,90,590,155),fill=(245,245,245))
        elif state=="battle":
            # Untrained non-board encounter shape: dual HUD over a dark arena.
            d.rectangle((100,40,1180,780),fill=(45,45,48))
            d.rectangle((430,50,650,190),fill=(190,20,20))
            d.rectangle((650,50,900,190),fill=(15,60,210))
            d.rectangle((500,90,590,155),fill=(245,245,245))
        return im
    def classify(self,state):
        with tempfile.NamedTemporaryFile(suffix=".png") as f:
            self.make_image(state).save(f.name)
            return agent.observe(f.name)
    def test_known_state_classes(self):
        for state in ("map","roulette","dialogue","barrier_choice","map_after_move"):
            with self.subTest(state=state):
                self.assertEqual(self.classify(state)["state"],state)
    def test_board_with_dual_hud_is_transition_not_battle(self):
        out=self.classify("map_after_move")
        self.assertEqual(out["state"],"map_after_move")
        self.assertEqual(out["action"],"WAIT")

    def test_three_card_overlay_is_card_selection_and_fails_closed(self):
        out=self.classify("card_selection")
        self.assertEqual(out["state"],"card_selection")
        self.assertEqual(out["action"],"WAIT")
        self.assertGreaterEqual(out["features"]["card_overlay_white"],.12)
        self.assertGreaterEqual(out["features"]["card_overlay_gray"],.16)

    def test_card_overlay_with_dialogue_prompt_stays_card_selection(self):
        out=self.classify("card_selection_with_dialogue")
        self.assertGreaterEqual(out["features"]["dialogue_orange"],.05)
        self.assertGreaterEqual(out["features"]["card_overlay_white"],.12)
        self.assertGreaterEqual(out["features"]["card_overlay_gray"],.16)
        self.assertEqual(out["state"],"card_selection")
        self.assertEqual(out["action"],"WAIT")

    def test_battle_screen_fails_closed_until_policy_calibrated(self):
        out=self.classify("battle")
        self.assertEqual(out["state"],"battle_untrained")
        self.assertEqual(out["action"],"WAIT")

    def test_unknown_fails_closed(self):
        out=self.classify("unknown")
        self.assertEqual(out["state"],"unknown")
        self.assertEqual(out["action"],"WAIT")
    def test_dialogue_uses_start(self):
        self.assertEqual(self.classify("dialogue")["action"],"START")

    def test_sparse_dialogue_box_uses_start_before_text_renders(self):
        out=self.classify("sparse_dialogue")
        self.assertEqual(out["state"],"dialogue")
        self.assertEqual(out["action"],"START")
    def test_yes_highlight_uses_contextual_circle(self):
        out=self.classify("barrier_choice")
        self.assertTrue(out["features"]["yes_selected_visual"])
        self.assertEqual(out["action"],"CIRCLE")

    def test_restore_only_gate_precedes_any_button_mutation(self):
        # This is an integration-level source regression for the Lua input path:
        # the guard must cover both ordinary frame-30 policy actions and the
        # direct START dialogue path, before button lookup or pad.setOverride.
        repo = Path(__file__).resolve().parents[1]
        workflow = (repo / ".github" / "workflows" / "naruto-storymode-adaptive-player.yml").read_text(encoding="utf-8")
        self.assertIn('local restoreTest=os.getenv("RESTORE_TEST")=="1"', workflow)
        self.assertIn('sendAction(plannedAction[cycle] or "WAIT",cycle)', workflow)
        self.assertIn('sendAction("START",cycle)', workflow)
        start = workflow.index("local function sendAction(action,cycle)")
        end = workflow.index("local function releaseAction(cycle)", start)
        send_action = workflow[start:end]
        guard = send_action.index("if restoreTest then")
        button_lookup = send_action.index("local b=buttons[action]")
        pad_mutation = send_action.index("pad.setOverride(b)")
        self.assertLess(guard, button_lookup)
        self.assertLess(guard, pad_mutation)
        guard_block = send_action[guard:button_lookup]
        self.assertIn("ADAPTIVE_RESTORE_ONLY_INPUT_SUPPRESSED", guard_block)
        self.assertIn("return", guard_block)
        # The guard is action-agnostic, so all three calibrated action families
        # (route movement, dialogue START, and contextual CIRCLE) are suppressed.
        for action in ("DOWN", "START", "CIRCLE"):
            with self.subTest(action=action):
                self.assertNotIn(f'action=="{action}"', guard_block)
        self.assertIn("ADAPTIVE_RESTORE_ONLY_NO_INPUT_ASSERT=PASS", workflow)


    def test_card_selection_ab_probe_accepts_only_circle_and_wait_control(self):
        repo = Path(__file__).resolve().parents[1]
        workflow = (repo / ".github" / "workflows" / "naruto-storymode-adaptive-player.yml").read_text(encoding="utf-8")
        self.assertIn('|| "$ab_expected_state" == "card_selection"', workflow)
        self.assertIn('elif [ "$ab_expected_state" = "card_selection" ]; then\n              [[ "$ab_action" == "CIRCLE" ]]', workflow)
        self.assertIn('local cardAction=(abAction=="CIRCLE")', workflow)
        self.assertIn('(abExpectedState=="card_selection" and cardAction)', workflow)
        self.assertIn('(state=="card_selection" and action=="WAIT")', workflow)
        self.assertIn("ADAPTIVE_POLICY_GUARD=PASS cycle=2 state=card_selection action=WAIT", workflow)
        # The A/B workflow must also check the no-input branch and button readback;
        # no gameplay experiment can rely only on the action branch's result.
        self.assertIn('grep -q "ADAPTIVE_INPUT cycle=1 action=$AB_ACTION phase=press readback=true status=PASS"', workflow)
        self.assertIn('grep -q \'ADAPTIVE_INPUT cycle=2 action=WAIT status=PASS reason=no_input_policy\'', workflow)

    def test_persistent_map_rotates_direction(self):
        with tempfile.TemporaryDirectory() as td:
            h=Path(td)/"history.json"
            h.write_text('{"last_state":"map","last_action":"DOWN","roulette_wait_count":0}')
            with tempfile.NamedTemporaryFile(suffix=".png") as f:
                self.make_image("map").save(f.name)
                self.assertEqual(agent.decide(f.name,h)["action"],"RIGHT")

if __name__=="__main__":
    unittest.main()
