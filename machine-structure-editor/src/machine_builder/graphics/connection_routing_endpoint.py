"""Endpoint escape routing for visual connections."""

from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF


def build_endpoint_stub(
    port_position: QPointF,
    side: str,
    stub_length: float,
) -> tuple[QPointF, str]:
    """Return the traditional straight outward stub."""
    normalized = _normalize_side(side)

    if normalized == "left":
        return (
            QPointF(
                port_position.x() - stub_length,
                port_position.y(),
            ),
            "horizontal",
        )

    if normalized == "right":
        return (
            QPointF(
                port_position.x() + stub_length,
                port_position.y(),
            ),
            "horizontal",
        )

    if normalized == "top":
        return (
            QPointF(
                port_position.x(),
                port_position.y() - stub_length,
            ),
            "vertical",
        )

    if normalized == "bottom":
        return (
            QPointF(
                port_position.x(),
                port_position.y() + stub_length,
            ),
            "vertical",
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
) -> tuple[list[QPointF], str]:
    """Escape from a port using a straight path or a dogleg.

    For a blocked horizontal departure, upward escape is preferred.
    Downward escape is the fallback.
    """

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

    stub_end, _ = build_endpoint_stub(
        port_position,
        normalized,
        stub_length,
    )

    direct = [
        port_position,
        stub_end,
    ]

    if _candidate_is_clear(
        direct,
        active_obstacles,
    ):
        return (
            direct,
            normalized,
        )

    blocking = _blocking_obstacles(
        port_position,
        stub_end,
        active_obstacles,
    )

    if not blocking:
        return (
            direct,
            normalized,
        )

    candidates = _build_escape_candidates(
        port_position=port_position,
        stub_end=stub_end,
        side=normalized,
        blocking=blocking,
        clearance=escape_clearance,
    )

    for candidate in candidates:
        if _candidate_is_clear(
            candidate,
            active_obstacles,
        ):
            return (
                candidate,
                normalized,
            )

    return (
        direct,
        normalized,
    )


def _build_escape_candidates(
    *,
    port_position: QPointF,
    stub_end: QPointF,
    side: str,
    blocking: list[QRectF],
    clearance: float,
) -> list[list[QPointF]]:
    """Build escape candidates in preferred order."""

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

        if side == "right":
            far_x = max(
                stub_end.x(),
                max(
                    rect.right()
                    for rect in blocking
                )
                + clearance,
            )
        else:
            far_x = min(
                stub_end.x(),
                min(
                    rect.left()
                    for rect in blocking
                )
                - clearance,
            )

        # UP first. This is the deliberate preference for now.
        return [
            [
                port_position,
                QPointF(
                    port_position.x(),
                    up_y,
                ),
                QPointF(
                    far_x,
                    up_y,
                ),
            ],
            [
                port_position,
                QPointF(
                    port_position.x(),
                    down_y,
                ),
                QPointF(
                    far_x,
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

    if side == "top":
        far_y = min(
            stub_end.y(),
            min(
                rect.top()
                for rect in blocking
            )
            - clearance,
        )
    else:
        far_y = max(
            stub_end.y(),
            max(
                rect.bottom()
                for rect in blocking
            )
            + clearance,
        )

    return [
        [
            port_position,
            QPointF(
                left_x,
                port_position.y(),
            ),
            QPointF(
                left_x,
                far_y,
            ),
        ],
        [
            port_position,
            QPointF(
                right_x,
                port_position.y(),
            ),
            QPointF(
                right_x,
                far_y,
            ),
        ],
    ]


def _candidate_is_clear(
    route: list[QPointF],
    obstacles: list[QRectF],
) -> bool:
    """Validate an escape route.

    The first segment may begin inside an overlapping obstacle, but it must
    actually escape that obstacle. Every later segment must be clear.
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

        if index != 0:
            return False

        # The first segment is allowed to leave an obstacle that already
        # contains the port. It is not allowed to enter a new obstacle.
        for rect in blocking:
            if not _point_inside(
                start,
                rect,
            ):
                return False

    return True


def _blocking_obstacles(
    start: QPointF,
    end: QPointF,
    obstacles: list[QRectF],
) -> list[QRectF]:
    return [
        rect
        for rect in obstacles
        if _point_inside(
            start,
            rect,
        )
        or _segment_blocked(
            start,
            end,
            [rect],
        )
    ]


def _point_inside_any(
    point: QPointF,
    obstacles: list[QRectF],
) -> bool:
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
    return (
        rect.left() < point.x() < rect.right()
        and rect.top() < point.y() < rect.bottom()
    )


def _segment_blocked(
    start: QPointF,
    end: QPointF,
    obstacles: list[QRectF],
) -> bool:
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
            rect.top() < y < rect.bottom()
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
            rect.left() < x < rect.right()
            and bottom > rect.top()
            and top < rect.bottom()
            for rect in obstacles
        )

    return True


def _is_ignored(
    obstacle: QRectF,
    ignored: list[QRectF],
) -> bool:
    return any(
        obstacle == candidate
        for candidate in ignored
    )


def _normalize_side(
    side: str,
) -> str:
    normalized = side.lower().strip()

    if normalized in {
        "left",
        "right",
        "top",
        "bottom",
    }:
        return normalized

    return "none"