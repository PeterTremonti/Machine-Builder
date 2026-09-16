"""Semantic values with explicit information status."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class SemanticValueStatus(str, Enum):
    """Status describing what is known about a semantic value."""

    ABSENT = "absent"
    UNKNOWN = "unknown"
    UNSPECIFIED = "unspecified"
    NOT_APPLICABLE = "not_applicable"
    KNOWN = "known"
    MEASURED = "measured"
    DERIVED = "derived"
    INFERRED = "inferred"
    CONFIGURED = "configured"
    CALIBRATED = "calibrated"


@dataclass(frozen=True)
class SemanticValue:
    """A value together with its semantic information status."""

    status: SemanticValueStatus
    value: Any = None

    def __post_init__(self) -> None:
        """Validate consistency between status and value."""
        value_required = {
            SemanticValueStatus.KNOWN,
            SemanticValueStatus.MEASURED,
            SemanticValueStatus.DERIVED,
            SemanticValueStatus.INFERRED,
            SemanticValueStatus.CONFIGURED,
            SemanticValueStatus.CALIBRATED,
        }

        value_forbidden = {
            SemanticValueStatus.ABSENT,
            SemanticValueStatus.UNKNOWN,
            SemanticValueStatus.UNSPECIFIED,
            SemanticValueStatus.NOT_APPLICABLE,
        }

        if (
            self.status in value_required
            and self.value is None
        ):
            raise ValueError(
                f"Status '{self.status.value}' "
                "requires a value."
            )

        if (
            self.status in value_forbidden
            and self.value is not None
        ):
            raise ValueError(
                f"Status '{self.status.value}' "
                "cannot contain a value."
            )

    @property
    def has_value(self) -> bool:
        """Return whether this semantic value contains an actual value."""
        return self.value is not None