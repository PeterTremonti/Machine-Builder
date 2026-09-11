"""Provisional port compatibility rules for the Machine Structure Editor.

This module intentionally contains only a small prototype ruleset.

It is not the canonical Machine Builder compatibility ontology.  Its purpose
is to provide immediate feedback while testing the visual connection
interaction.

Compatibility results are deliberately more expressive than a simple
True/False value so that unknown information is not mistaken for confirmed
compatibility.
"""

from __future__ import annotations

from enum import Enum

from .visual_model import VisualPort


class CompatibilityResult(str, Enum):
    """Possible results from the provisional compatibility engine."""

    COMPATIBLE = "compatible"
    INCOMPATIBLE = "incompatible"
    UNKNOWN = "unknown"
    CONDITIONAL = "conditional"


def check_port_compatibility(
    source: VisualPort,
    target: VisualPort,
) -> CompatibilityResult:
    """Evaluate whether two visual ports can be connected.

    The first prototype supports only deliberately simple rules:

    * signal output → signal input: compatible
    * electrical output/input combinations: conditionally compatible
    * electrical → signal: incompatible
    * signal → electrical: incompatible
    * matching unknown types: unknown
    * unknown type information: unknown

    Direction is treated as useful information but is not allowed to create
    a false sense of certainty when the type itself is unknown.
    """
    source_type = source.port_type.lower().strip()
    target_type = target.port_type.lower().strip()

    source_direction = source.direction.lower().strip()
    target_direction = target.direction.lower().strip()

    if source.id == target.id:
        return CompatibilityResult.INCOMPATIBLE

    if source_type == "unknown" or target_type == "unknown":
        return CompatibilityResult.UNKNOWN

    if source_type == "signal" and target_type == "signal":
        if (
            source_direction == "output"
            and target_direction == "input"
        ):
            return CompatibilityResult.COMPATIBLE

        if (
            source_direction == "input"
            and target_direction == "output"
        ):
            return CompatibilityResult.INCOMPATIBLE

        return CompatibilityResult.UNKNOWN

    if source_type == "electrical" and target_type == "electrical":
        if (
            source_direction == "output"
            and target_direction == "input"
        ):
            return CompatibilityResult.CONDITIONAL

        if (
            source_direction == "input"
            and target_direction == "output"
        ):
            return CompatibilityResult.CONDITIONAL

        return CompatibilityResult.UNKNOWN

    if source_type == "electrical" and target_type == "signal":
        return CompatibilityResult.INCOMPATIBLE

    if source_type == "signal" and target_type == "electrical":
        return CompatibilityResult.INCOMPATIBLE

    if source_type == target_type:
        return CompatibilityResult.UNKNOWN

    return CompatibilityResult.INCOMPATIBLE