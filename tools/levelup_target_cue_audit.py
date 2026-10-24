"""Offline-only metrics for the known map selection reference signature.

This module is deliberately not imported by the gameplay decision policy. A matching
map-context signature is evidence for regression calibration only; it does not verify
the nested level-up submenu target and never authorizes controller input.
"""
from __future__ import annotations

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
