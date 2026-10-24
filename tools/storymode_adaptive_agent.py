#!/usr/bin/env python3
"""Conservative screenshot-driven policy for Naruto PS1 Story Mode.

Only calibrated visual states can cause input. Unrecognized states fail closed.
Screenshots and savestates stay in private Actions artifacts, never in Git.
"""
from __future__ import annotations
import argparse, json, os, re, subprocess
from pathlib import Path
from typing import Any
import numpy as np
from PIL import Image

VERSION = "0.4.0"

def _ratios(image: np.ndarray, box: tuple[int,int,int,int]) -> dict[str, float]:
    x1,y1,x2,y2=box
    c=image[y1:y2,x1:x2,:].astype(np.int16)
    r,g,b=c[:,:,0],c[:,:,1],c[:,:,2]
    total=float(c.shape[0]*c.shape[1]) or 1.0
    masks={
        "red":(r>100)&(r>g*1.25)&(r>b*1.15),
        "gold":(r>100)&(g>60)&(r>g*1.15)&(g>b*1.25),
        "green":(g>r*1.12)&(g>b*1.05)&(g>45),
        "blue":(b>90)&(b>r*1.25)&(b>g*1.1),
        "white":(r>190)&(g>190)&(b>190),
        "orange":(r>100)&(g>45)&(r>g*1.18)&(g>b*1.15)&(b<140),
        # Card backs have a substantial low-chroma gray lattice plus bright frame.
        "gray":(np.max(c,axis=2)-np.min(c,axis=2)<24)&(np.mean(c,axis=2)>35)&(np.mean(c,axis=2)<180),
    }
    return {k:float(np.count_nonzero(v)/total) for k,v in masks.items()}

def _ocr_digits(image: np.ndarray, box: tuple[int,int,int,int]) -> int | None:
    """Optional best-effort OCR, included as evidence but never used to guess."""
    try:
        import shutil
        if shutil.which("tesseract") is None:
            return None
        x1,y1,x2,y2=box
        im=Image.fromarray(image[y1:y2,x1:x2,:].astype(np.uint8)).resize(((x2-x1)*7,(y2-y1)*7))
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            tmp=f.name
        try:
            im.save(tmp)
            r=subprocess.run(["tesseract",tmp,"stdout","-l","eng","--psm","7","-c","tessedit_char_whitelist=0123456789"],capture_output=True,text=True,timeout=3)
            digits=re.sub(r"\D","",r.stdout)
            if r.returncode or not digits or len(digits)>4:
                return None
            return int(digits)
        finally:
            try: os.unlink(tmp)
            except OSError: pass
    except Exception:
        return None

def observe(path: str | Path) -> dict[str, Any]:
    with Image.open(path) as source:
        im=source.convert("RGB")
        if im.size != (1280,800):
            return {"state":"unknown","confidence":0.0,"action":"WAIT","reason":"unexpected_image_size","image_size":list(im.size),"version":VERSION}
        arr=np.asarray(im)
    wheel=_ratios(arr,(100,70,700,730))
    dialogue_box=_ratios(arr,(130,515,1150,740))
    # Genuine spoken-dialogue panels use a full-width ornate top border/portrait;
    # the barrier-upgrade submenu uses a smaller left panel and footer controls.
    dialogue_header=_ratios(arr,(130,510,1150,580))
    prompt_footer=_ratios(arr,(650,680,1140,770))
    choice=_ratios(arr,(920,550,1130,690))
    choice_top=_ratios(arr,(920,555,1130,625))
    choice_bottom=_ratios(arr,(920,625,1130,690))
    center_number=_ratios(arr,(550,375,730,480))
    center=_ratios(arr,(400,180,900,680))
    # Calibrated against authentic encounter frames from adaptive run 39687675432.
    top_hud=_ratios(arr,(380,30,920,225))
    menu=_ratios(arr,(1000,220,1275,560))
    card_overlay=_ratios(arr,(370,220,930,530))
    central_card=_ratios(arr,(500,220,780,535))
    card_art=_ratios(arr,(545,245,730,380))
    # This small footer ROI isolates the Circle confirm glyph shown when a
    # revealed card is actionable; the broader instruction panel is not enough.
    card_confirm_glyph=_ratios(arr,(1030,665,1105,712))
    features={
        "wheel_red":round(wheel["red"],4),"wheel_gold":round(wheel["gold"],4),
        "dialogue_orange":round(dialogue_box["orange"],4),"dialogue_white":round(dialogue_box["white"],4),
        "dialogue_header_orange":round(dialogue_header["orange"],4),
        "prompt_footer_red":round(prompt_footer["red"],4),"prompt_footer_blue":round(prompt_footer["blue"],4),
        "choice_red":round(choice["red"],4),"choice_blue":round(choice["blue"],4),
        "choice_top_red":round(choice_top["red"],4),"choice_bottom_red":round(choice_bottom["red"],4),
        "center_number_blue":round(center_number["blue"],4),"center_green":round(center["green"],4),
        "menu_white":round(menu["white"],4),"menu_orange":round(menu["orange"],4),
        "top_hud_red":round(top_hud["red"],4),"top_hud_blue":round(top_hud["blue"],4),
        "top_hud_white":round(top_hud["white"],4),
        "card_overlay_white":round(card_overlay["white"],4),
        "card_overlay_gray":round(card_overlay["gray"],4),
        "central_card_gray":round(central_card["gray"],4),
        "card_art_blue":round(card_art["blue"],4),
        "card_art_white":round(card_art["white"],4),
        "card_confirm_glyph_red":round(card_confirm_glyph["red"],4),
    }

    # Priority matters: the wheel can cover a map, and a real dialogue frame may have a
    # visible gold box before Japanese text has finished rendering. Cutoffs are checked against authentic X11 frames.
    if wheel["red"] >= .22 and wheel["gold"] >= .10:
        state,conf,reason="roulette",.98,"calibrated_wheel_color_signature"
    elif choice["red"] >= .12 and choice["blue"] >= .04 and center_number["blue"] >= .14:
        yes=(choice_top["red"] >= .16 and choice_top["red"] > choice_bottom["red"]*1.5)
        state,conf,reason="barrier_choice",.94,"choice_panel_and_blue_120_cost_signature"
        chakra=_ocr_digits(arr,(500,90,660,165))
        features["yes_selected_visual"]=bool(yes)
        features["chakra_ocr_best_effort"]=chakra
        features["required_chakra_calibrated"]=120
    elif card_art["blue"] >= .25 and card_art["white"] >= .40 and central_card["gray"] <= .12:
        # The revealed card alone is not sufficient: intermediate reveal animation
        # can show similar art without the lower-right Circle confirm glyph.
        # Only the independently A/B-verified stable card-detail + Circle cue can
        # authorize a confirmation; otherwise retain a distinct WAIT state.
        if card_confirm_glyph["red"] >= .12:
            state,conf,reason="card_selection_detail",.97,"revealed_card_art_with_circle_confirm_glyph"
        else:
            state,conf,reason="card_selection_detail_unconfirmed",.90,"revealed_card_art_without_clear_circle_confirm_glyph"
    elif card_overlay["white"] >= .12 and card_overlay["gray"] >= .16:
        # Card backs and card prompts outrank generic dialogue; START would bypass them.
        state,conf,reason="card_selection",.97,"three_card_back_overlay_white_frame_gray_lattice"
    elif (dialogue_box["orange"] >= .04 and dialogue_box["orange"] < .10
          and dialogue_header["orange"] < .05
          and center["green"] >= .42
          and top_hud["red"] >= .05 and top_hud["blue"] >= .05 and top_hud["white"] >= .035
          and prompt_footer["red"] >= .05 and prompt_footer["blue"] >= .008):
        # Revision58 authentic F60/F100/F110 frames show a smaller lower-left
        # instruction panel and explicit Circle-confirm / X-back glyphs. This is
        # not story dialogue; treating it as dialogue incorrectly presses START.
        state,conf,reason="barrier_level_selection",.93,"calibrated_small_barrier_selection_panel_with_circle_x_footer"
    elif dialogue_box["orange"] >= .07 and dialogue_header["orange"] >= .08:
        state,conf,reason="dialogue",.93,"full_width_ornate_dialogue_panel_signature"
    elif menu["white"] >= .06 and menu["orange"] >= .025:
        state,conf,reason="menu_or_unknown_choice",.78,"right_side_menu_requires_context"
    elif center["green"] >= .42 and wheel["red"] < .10 and top_hud["red"] >= .05 and top_hud["blue"] >= .05 and top_hud["white"] >= .035:
        # Authentic frames show the board, route/tile objects and both HUDs after a move.
        # This is a board-transition signature, not sufficient evidence of a battle.
        state,conf,reason="map_after_move",.90,"green_board_with_dual_HUD_transition_signature"
    elif top_hud["red"] >= .05 and top_hud["blue"] >= .05 and top_hud["white"] >= .035:
        # A dual HUD alone is not enough to infer combat mechanics.
        state,conf,reason="battle_untrained",.80,"dual_character_HUD_without_calibrated_board_signature"
    elif center["green"] >= .42 and wheel["red"] < .10:
        state,conf,reason="map",.88,"calibrated_green_map_and_no_wheel_signature"
    else:
        state,conf,reason="unknown",0.0,"no_calibrated_state_signature"

    action,action_reason="WAIT","fail_closed_or_observe_again"
    if state=="dialogue":
        action,action_reason="START","verified_story_dialogue_skip_policy"
    elif state=="barrier_choice":
        if features.get("yes_selected_visual"):
            action,action_reason="CIRCLE","calibrated_barrier_prompt_with_YES_visibly_highlighted_and_120_cost"
        else:
            action_reason="choice_not_verified_as_YES_highlighted"
    elif state=="card_selection_detail":
        # Authentic Circle-vs-WAIT A/B: a stable revealed card with the Circle
        # confirm glyph advanced to dialogue/map; the no-input control did not.
        action,action_reason="CIRCLE","verified_revealed_card_detail_with_circle_confirm_glyph"
    elif state=="card_selection_detail_unconfirmed":
        action,action_reason="WAIT","revealed_card_confirmation_glyph_not_verified"
    elif state=="barrier_level_selection":
        # The prompt documents Circle as confirm, but no selected target is yet
        # visually identified. Wait for a controlled direction/selection probe.
        action,action_reason="WAIT","barrier_target_not_identified; fail_closed_until_controlled_probe"
    elif state=="roulette":
        action,action_reason="WAIT","let_wheel_settle_before_input"
    elif state=="map":
        action,action_reason="DOWN","first_route step; later directions rotate if map persists"
    return {"state":state,"confidence":conf,"reason":reason,"action":action,"action_reason":action_reason,"features":features,"version":VERSION}

def decide(path: str | Path, history_path: str | Path | None = None) -> dict[str, Any]:
    result=observe(path)
    history={}
    if history_path and Path(history_path).exists():
        try: history=json.loads(Path(history_path).read_text(encoding="utf-8"))
        except Exception: history={}
    directions=["DOWN","RIGHT","UP","LEFT"]
    last_action,last_state=history.get("last_action"),history.get("last_state")
    if result["state"]=="map" and last_state=="map" and last_action in directions:
        result["action"]=directions[(directions.index(last_action)+1)%len(directions)]
        result["action_reason"]="map persisted after prior direction; controlled next-direction probe"
    elif result["state"]=="roulette" and int(history.get("roulette_wait_count",0))>=1:
        result["action"]="CIRCLE"
        result["action_reason"]="wheel remained visible after a full no-input observation window"
    if result["state"]=="roulette":
        result["roulette_wait_count"]=int(history.get("roulette_wait_count",0))+(1 if result["action"]=="WAIT" else 0)
    else:
        result["roulette_wait_count"]=0
    result["previous_state"]=last_state
    result["previous_action"]=last_action
    result["history"]={"last_state":result["state"],"last_action":result["action"],"roulette_wait_count":result["roulette_wait_count"]}
    return result

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("image")
    p.add_argument("--history",default=None)
    p.add_argument("--output",default=None)
    a=p.parse_args()
    result=decide(a.image,a.history)
    out=json.dumps(result,ensure_ascii=False,sort_keys=True)
    print(out)
    if a.output: Path(a.output).write_text(out+"\n",encoding="utf-8")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
