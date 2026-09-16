"""Complete persistent editor state.

The editor state contains both the visual representation and the canonical
semantic machine model.
"""

from __future__ import annotations

from dataclasses import dataclass

from .semantic_model import CanonicalMachineModel
from .visual_model import VisualModel


@dataclass
class EditorState:
    """Complete persistent state for the Machine Structure Editor."""

    visual_model: VisualModel
    semantic_model: CanonicalMachineModel