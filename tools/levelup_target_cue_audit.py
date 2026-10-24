"""Offline-only metrics for the known map selection reference signature.

This module is deliberately not imported by the gameplay decision policy. A matching
map-context signature is evidence for regression calibration only; it does not verify
the nested level-up submenu target and never authorizes controller input.
"""
from __future__ import annotations

import math

RING_MIN_PIXELS = 500
STATS_PANEL_GOLD_MIN_PIXELS = 5000
PANEL_TEXT_DELTA_MIN_PIXELS = 100


def matches_map_selection_reference(
    ring_pixels: int | None,
    stats_panel_gold_pixels: int | None,
    panel_text_delta_pixels: int | None,
) -> bool:
    """Return whether all three calibrated map-context features are present.

    Missing, malformed, negative, or boolean inputs fail closed. The gold-panel
    footprint is a required precondition so camera-pan changes in the same screen
    ROI cannot masquerade as statistics-panel content updates.
    """
    metrics = (ring_pixels, stats_panel_gold_pixels, panel_text_delta_pixels)
    if any(
        value is None
        or isinstance(value, bool)
        or not isinstance(value, int)
        or value < 0
        for value in metrics
    ):
        return False
    return (
        ring_pixels >= RING_MIN_PIXELS
        and stats_panel_gold_pixels >= STATS_PANEL_GOLD_MIN_PIXELS
        and panel_text_delta_pixels >= PANEL_TEXT_DELTA_MIN_PIXELS
    )

BADGE_PULSE_RGB_DISTANCE_MAX = 12.0


def same_badge_pulse_across_contexts(
    up_rgb_means: dict[str, tuple[float, float, float]] | None,
    wait_rgb_means: dict[str, tuple[float, float, float]] | None,
    max_distance: float = BADGE_PULSE_RGB_DISTANCE_MAX,
) -> bool:
    """Return whether the same-frame badge pulse is shared by UP and WAIT.

    This is a negative cue discriminator, not a target detector. If the candidate
    badge has nearly the same RGB pulse phase in different selection contexts,
    color/brightness alone cannot tell whether that tile is selected. Malformed,
    missing, non-finite, or mismatched frame data fails closed.
    """
    if (
        not isinstance(up_rgb_means, dict)
        or not isinstance(wait_rgb_means, dict)
        or not up_rgb_means
        or up_rgb_means.keys() != wait_rgb_means.keys()
        or isinstance(max_distance, bool)
        or not isinstance(max_distance, (int, float))
        or not math.isfinite(float(max_distance))
        or max_distance < 0
    ):
        return False
    for frame in up_rgb_means:
        up, wait = up_rgb_means[frame], wait_rgb_means[frame]
        if not isinstance(up, (tuple, list)) or not isinstance(wait, (tuple, list)) or len(up) != 3 or len(wait) != 3:
            return False
        if any(
            isinstance(channel, bool)
            or not isinstance(channel, (int, float))
            or not math.isfinite(float(channel))
            for channel in (*up, *wait)
        ):
            return False
        distance = math.sqrt(sum((float(a) - float(b)) ** 2 for a, b in zip(up, wait)))
        if distance > max_distance:
            return False
    return True

