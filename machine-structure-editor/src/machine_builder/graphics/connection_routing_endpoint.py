"""Endpoint escape routing for visual connections."""

from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF


def build_endpoint_stub(
    port_position: QPointF,
    side: str,
    stub_length: float,
) -> tuple[QPointF, str]:
    """Return the fixed outward endpoint stub."""
    normalized = _normalize_side(side)

    if normalized == "left":
        return (
            QPointF(
                port_position.x() - stub_length,
                port_position.y(),
            ),
            "left",
        )

    if normalized == "right":
        return (
            QPointF(
                port_position.x() + stub_length,
                port_position.y(),
            ),
            "right",
        )

    if normalized == "top":
        return (
            QPointF(
                port_position.x(),
                port_position.y() - stub_length,
            ),
            "up",
        )

    if normalized == "bottom":
        return (
            QPointF(
                port_position.x(),
                port_position.y() + stub_length,
            ),
            "down",
        )

    return (
        port_position,
        "none",
    )


def build_endpoint_escape(
    *,
    port_position: QPointF,
    side: str,
    obstacles: list[QRectF],
    stub_length: float,
    escape_clearance: float,
    ignored_obstacles: list[QRectF],
    preferred_escape_direction: str | None = None,
    allow_escape_reselection: bool = True,
    escape_hysteresis_ratio: float = 0.20,
    escape_hysteresis_distance: float = 24.0,
) -> tuple[list[QPointF], str]:
    """Build a fixed outward stub or an obstacle escape."""

    normalized = _normalize_side(side)

    if normalized == "none":
        return (
            [port_position],
            "none",
        )

    active_obstacles = [
        obstacle
        for obstacle in obstacles
        if not _is_ignored(
            obstacle,
            ignored_obstacles,
        )
    ]

    stub_end, direction = build_endpoint_stub(
        port_position,
        normalized,
        stub_length,
    )

    fixed_stub = [
        port_position,
        stub_end,
    ]

    # Determine whether the fixed stub is actually blocked.
    #
    # Do not use _candidate_is_clear() here because that helper
    # intentionally permits the first segment to overlap an improperly
    # placed component. That behavior is correct when validating an
    # escape candidate, but it would incorrectly classify a blocked
    # fixed stub as clear and prevent escape generation.
    blocking = _blocking_obstacles(
        port_position,
        stub_end,
        active_obstacles,
    )

    if not blocking:
        return (
            fixed_stub,
            direction,
        )

    candidates = _build_escape_candidates(
        port_position=port_position,
        stub_end=stub_end,
        side=normalized,
        blocking=blocking,
        clearance=escape_clearance,
    )

    clear_candidates = [
        candidate
        for candidate in candidates
        if _candidate_is_clear(
            candidate,
            active_obstacles,
        )
    ]

    if clear_candidates:
        selected = _choose_escape_candidate(
            clear_candidates,
            preferred_direction=preferred_escape_direction,
            allow_reselection=allow_escape_reselection,
            improvement_ratio=escape_hysteresis_ratio,
            minimum_improvement=escape_hysteresis_distance,
        )

        return (
            selected,
            direction,
        )

    # The placement is probably invalid. Preserve the fixed stub instead
    # of moving the component or inventing an arbitrary route.
    return (
        fixed_stub,
        direction,
    )


def _escape_candidate_direction(
    candidate: list[QPointF],
) -> str:
    """Return the direction of the candidate's escape turn."""
    if len(candidate) < 3:
        return "none"

    start = candidate[-2]
    end = candidate[-1]

    if abs(end.x() - start.x()) >= 0.001:
        return (
            "right"
            if end.x() > start.x()
            else "left"
        )

    if abs(end.y() - start.y()) >= 0.001:
        return (
            "down"
            if end.y() > start.y()
            else "up"
        )

    return "none"


def _escape_candidate_distance(
    candidate: list[QPointF],
) -> float:
    """Return the distance traveled after the fixed stub."""
    if len(candidate) < 3:
        return 0.0

    return sum(
        abs(
            candidate[index + 1].x()
            - candidate[index].x()
        )
        + abs(
            candidate[index + 1].y()
            - candidate[index].y()
        )
        for index in range(
            1,
            len(candidate) - 1,
        )
    )


def _choose_escape_candidate(
    candidates: list[list[QPointF]],
    *,
    preferred_direction: str | None,
    allow_reselection: bool,
    improvement_ratio: float,
    minimum_improvement: float,
) -> list[QPointF]:
    """Choose the nearest escape while honoring hysteresis."""
    if not candidates:
        raise ValueError(
            "At least one escape candidate is required."
        )

    best = min(
        candidates,
        key=_escape_candidate_distance,
    )

    if not preferred_direction:
        return best

    preferred = next(
        (
            candidate
            for candidate in candidates
            if _escape_candidate_direction(candidate)
            == preferred_direction
        ),
        None,
    )

    if preferred is None:
        return best

    if preferred is best:
        return preferred

    if not allow_reselection:
        return preferred

    preferred_distance = _escape_candidate_distance(
        preferred,
    )

    best_distance = _escape_candidate_distance(
        best,
    )

    improvement = (
        preferred_distance
        - best_distance
    )

    if (
        improvement >= minimum_improvement
        and best_distance
        <= preferred_distance
        * (
            1.0
            - improvement_ratio
        )
    ):
        return best

    return preferred


def _build_escape_candidates(
    *,
    port_position: QPointF,
    stub_end: QPointF,
    side: str,
    blocking: list[QRectF],
    clearance: float,
) -> list[list[QPointF]]:
    """Build local escapes that turn at the end of the fixed stub."""

    if side in {
        "right",
        "left",
    }:
        up_y = (
            min(
                rect.top()
                for rect in blocking
            )
            - clearance
        )

        down_y = (
            max(
                rect.bottom()
                for rect in blocking
            )
            + clearance
        )

        # Escape only perpendicular to the fixed stub.
        # The main route owns the global movement after this point.
        return [
            [
                port_position,
                stub_end,
                QPointF(
                    stub_end.x(),
                    up_y,
                ),
            ],
            [
                port_position,
                stub_end,
                QPointF(
                    stub_end.x(),
                    down_y,
                ),
            ],
        ]

    left_x = (
        min(
            rect.left()
            for rect in blocking
        )
        - clearance
    )

    right_x = (
        max(
            rect.right()
            for rect in blocking
        )
        + clearance
    )

    # Escape only perpendicular to the fixed stub.
    # The main route owns the global movement after this point.
    return [
        [
            port_position,
            stub_end,
            QPointF(
                left_x,
                stub_end.y(),
            ),
        ],
        [
            port_position,
            stub_end,
            QPointF(
                right_x,
                stub_end.y(),
            ),
        ],
    ]

def _candidate_is_clear(
    route: list[QPointF],
    obstacles: list[QRectF],
) -> bool:
    """Validate an endpoint escape.

    The first segment is allowed to pass through an improperly overlapping
    module because placement validation will handle that condition later.
    Once the wire reaches the end of its fixed stub, subsequent escape
    segments must be clear.
    """
    if len(route) < 2:
        return True

    if _point_inside_any(
        route[-1],
        obstacles,
    ):
        return False

    for index in range(
        len(route) - 1,
    ):
        start = route[index]
        end = route[index + 1]

        blocking = [
            rect
            for rect in obstacles
            if _segment_blocked(
                start,
                end,
                [rect],
            )
        ]

        if not blocking:
            continue

        # The fixed stub itself may overlap an improperly placed module.
        if index == 0:
            continue

        return False

    return True


def _blocking_obstacles(
    start: QPointF,
    end: QPointF,
    obstacles: list[QRectF],
) -> list[QRectF]:
    """Return obstacles intersecting the candidate fixed stub."""
    return [
        obstacle
        for obstacle in obstacles
        if _segment_blocked(
            start,
            end,
            [obstacle],
        )
    ]


def _segment_blocked(
    start: QPointF,
    end: QPointF,
    obstacles: list[QRectF],
) -> bool:
    """Return whether an orthogonal segment crosses any obstacle."""
    if (
        abs(start.x() - end.x()) < 0.001
        and abs(start.y() - end.y()) < 0.001
    ):
        return False

    if abs(start.y() - end.y()) < 0.001:
        y = start.y()

        left = min(
            start.x(),
            end.x(),
        )

        right = max(
            start.x(),
            end.x(),
        )

        return any(
            rect.top()
            < y
            < rect.bottom()
            and right > rect.left()
            and left < rect.right()
            for rect in obstacles
        )

    if abs(start.x() - end.x()) < 0.001:
        x = start.x()

        top = min(
            start.y(),
            end.y(),
        )

        bottom = max(
            start.y(),
            end.y(),
        )

        return any(
            rect.left()
            < x
            < rect.right()
            and bottom > rect.top()
            and top < rect.bottom()
            for rect in obstacles
        )

    # Endpoint escape geometry is expected to remain orthogonal.
    return True


def _point_inside_any(
    point: QPointF,
    obstacles: list[QRectF],
) -> bool:
    """Return whether a point lies strictly inside any obstacle."""
    return any(
        _point_inside(
            point,
            rect,
        )
        for rect in obstacles
    )


def _point_inside(
    point: QPointF,
    rect: QRectF,
) -> bool:
    """Return whether a point lies strictly inside a rectangle."""
    return (
        rect.left()
        < point.x()
        < rect.right()
        and rect.top()
        < point.y()
        < rect.bottom()
    )


def _is_ignored(
    obstacle: QRectF,
    ignored_obstacles: list[QRectF],
) -> bool:
    """Return whether an obstacle should be excluded from routing."""
    return any(
        obstacle == ignored
        for ignored in ignored_obstacles
    )


def _normalize_side(
    side: str,
) -> str:
    """Normalize endpoint side names."""
    normalized = str(side).strip().lower()

    aliases = {
        "l": "left",
        "left": "left",
        "r": "right",
        "right": "right",
        "t": "top",
        "top": "top",
        "up": "top",
        "b": "bottom",
        "bottom": "bottom",
        "down": "bottom",
    }

    return aliases.get(
        normalized,
        "none",
    )