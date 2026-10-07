"""End-to-end GUI validation for routing stability under precision nudging."""

from __future__ import annotations

import tempfile
from pathlib import Path

from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QApplication

from machine_builder.canvas import MachineCanvas
from machine_builder.document_controller import DocumentController


MACHINE_PATH = (
    Path(__file__).resolve().parents[1]
    / "wiring test machines"
    / "4 parts.machine.json"
)

REPORT_PATH = (
    Path(tempfile.gettempdir())
    / "machine_builder_routing_validation.txt"
)


def _application() -> QApplication:
    application = QApplication.instance()

    if application is None:
        application = QApplication([])

    return application


def _route_summary(
    route: tuple[QPointF, ...] | None,
) -> str:
    if route is None:
        return "none"

    return "[" + ", ".join(
        f"({point.x():.6f}, {point.y():.6f})"
        for point in route
    ) + "]"


def _route_topology(
    route: tuple[QPointF, ...] | None,
) -> tuple[str, ...] | None:
    if route is None or len(route) < 2:
        return None

    topology: list[str] = []

    for first, second in zip(
        route,
        route[1:],
    ):
        dx = second.x() - first.x()
        dy = second.y() - first.y()

        if abs(dx) < 1e-9 and abs(dy) >= 1e-9:
            topology.append("V")
        elif abs(dy) < 1e-9 and abs(dx) >= 1e-9:
            topology.append("H")
        else:
            topology.append("X")

    return tuple(topology)


def _same_points(
    first: tuple[QPointF, ...],
    second: tuple[QPointF, ...],
    tolerance: float = 1e-9,
) -> bool:
    if len(first) != len(second):
        return False

    return all(
        abs(a.x() - b.x()) <= tolerance
        and abs(a.y() - b.y()) <= tolerance
        for a, b in zip(first, second)
    )


def _write_report(lines: list[str]) -> None:
    REPORT_PATH.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def test_precision_nudge_routing_validation_real_machine() -> None:
    application = _application()
    canvas = MachineCanvas()
    lines: list[str] = []

    try:
        lines.extend(
            [
                "Machine Builder Routing Validation",
                "==================================",
                "",
                f"Machine file: {MACHINE_PATH}",
                f"Report file: {REPORT_PATH}",
                "Target node: node-2",
                "Target node label: Temperature Controller",
                "Target connection: connection-1",
                "Nudge direction: +X",
                "Nudge step: 0.001",
                "Nudge count: 10",
                "",
            ]
        )

        assert MACHINE_PATH.is_file()

        controller = DocumentController(
            canvas.store
        )
        canvas.document_controller = controller
        controller.open(MACHINE_PATH)

        application.processEvents()

        assert "node-2" in canvas._node_items
        assert "connection-1" in canvas._connection_items

        node_item = canvas._node_items["node-2"]
        connection_item = (
            canvas._connection_items["connection-1"]
        )
        inspector = canvas.selection_inspector

        canvas.scene.clearSelection()
        node_item.setSelected(True)
        application.processEvents()

        assert node_item.isSelected()

        inspector._nudge_step.setValue(0.001)
        assert inspector._nudge_step.value() == 0.001

        node = canvas.store.model.nodes["node-2"]
        initial_x = node.x
        initial_y = node.y

        baseline_route = tuple(
            connection_item._routing_selected_route
            or ()
        )
        baseline_topology = _route_topology(
            baseline_route
        )
        baseline_end_escape = tuple(
            connection_item._debug_end_escape
        )

        assert len(baseline_route) >= 2
        assert baseline_topology is not None

        lines.extend(
            [
                "Baseline",
                "--------",
                f"Node position: ({initial_x:.6f}, {initial_y:.6f})",
                f"Route topology: {baseline_topology}",
                (
                    "Selected route: "
                    f"{_route_summary(baseline_route)}"
                ),
                (
                    "End escape: "
                    f"{_route_summary(baseline_end_escape)}"
                ),
                f"Decision: {connection_item._routing_stability_reason}",
                "",
            ]
        )

        route_topology_failures = 0
        interior_geometry_failures = 0
        endpoint_motion_failures = 0
        stability_decision_failures = 0
        preferred_repairs = 0

        for step in range(1, 11):
            inspector._request_nudge(
                1.0,
                0.0,
            )

            application.processEvents()

            node = canvas.store.model.nodes["node-2"]

            current_route = tuple(
                connection_item._routing_selected_route
                or ()
            )
            current_topology = _route_topology(
                current_route
            )

            expected_x = (
                initial_x
                + (step * 0.001)
            )

            endpoint_motion_ok = (
                abs(node.x - expected_x) <= 1e-9
                and abs(node.y - initial_y) <= 1e-9
                and len(current_route)
                == len(baseline_route)
                and abs(
                    current_route[0].x()
                    - (baseline_route[0].x() + step * 0.001)
                ) <= 1e-9
                and abs(
                    current_route[0].y()
                    - baseline_route[0].y()
                ) <= 1e-9
            )

            topology_ok = (
                current_topology
                == baseline_topology
            )

            interior_geometry_ok = (
                len(current_route) >= 2
                and _same_points(
                    current_route[1:],
                    baseline_route[1:],
                )
            )

            stability_ok = (
                connection_item._routing_stability_reason
                == "previous stable route held within tolerance"
            )

            end_escape_ok = _same_points(
                tuple(connection_item._debug_end_escape),
                baseline_end_escape,
            )

            if not endpoint_motion_ok:
                endpoint_motion_failures += 1

            if not topology_ok:
                route_topology_failures += 1

            if not interior_geometry_ok or not end_escape_ok:
                interior_geometry_failures += 1

            if not stability_ok:
                stability_decision_failures += 1

            if (
                "preferred-spacing geometry repair"
                in connection_item._routing_stability_reason
            ):
                preferred_repairs += 1

            lines.extend(
                [
                    f"Step {step}",
                    f"------",
                    (
                        "Node position: "
                        f"({node.x:.6f}, {node.y:.6f})"
                    ),
                    f"Expected X: {expected_x:.6f}",
                    f"Topology stable: {topology_ok}",
                    (
                        "Interior geometry stable: "
                        f"{interior_geometry_ok}"
                    ),
                    (
                        "Endpoint motion correct: "
                        f"{endpoint_motion_ok}"
                    ),
                    (
                        "End escape stable: "
                        f"{end_escape_ok}"
                    ),
                    (
                        "Stability decision stable: "
                        f"{stability_ok}"
                    ),
                    (
                        "Selected route: "
                        f"{_route_summary(current_route)}"
                    ),
                    (
                        "Decision: "
                        f"{connection_item._routing_stability_reason}"
                    ),
                    "",
                ]
            )

            _write_report(lines)

        final_node = canvas.store.model.nodes["node-2"]

        expected_final_x = (
            initial_x + 0.010
        )

        assert abs(
            final_node.x - expected_final_x
        ) <= 1e-9

        assert abs(
            final_node.y - initial_y
        ) <= 1e-9

        assert route_topology_failures == 0
        assert interior_geometry_failures == 0
        assert endpoint_motion_failures == 0
        assert stability_decision_failures == 0

        final_route = tuple(
            connection_item._routing_selected_route
            or ()
        )

        assert len(final_route) >= 2
        assert _route_topology(final_route) == baseline_topology

        lines.extend(
            [
                "Validation Summary",
                "===================",
                f"Initial X: {initial_x:.6f}",
                f"Final X: {final_node.x:.6f}",
                f"Expected X: {expected_final_x:.6f}",
                f"Initial Y: {initial_y:.6f}",
                f"Final Y: {final_node.y:.6f}",
                (
                    "Topology failures: "
                    f"{route_topology_failures}"
                ),
                (
                    "Interior geometry failures: "
                    f"{interior_geometry_failures}"
                ),
                (
                    "Endpoint motion failures: "
                    f"{endpoint_motion_failures}"
                ),
                (
                    "Stability decision failures: "
                    f"{stability_decision_failures}"
                ),
                (
                    "Preferred-spacing repairs observed: "
                    f"{preferred_repairs}"
                ),
                f"Final route points: {len(final_route)}",
                "",
                "RESULT: PASS",
            ]
        )
        _write_report(lines)

        print(
            "Routing validation PASS — "
            f"report: {REPORT_PATH}"
        )

    except Exception as exc:
        lines.extend(
            [
                "",
                "RESULT: FAIL",
                f"{type(exc).__name__}: {exc}",
            ]
        )
        _write_report(lines)
        raise

    finally:
        canvas.close()
        application.processEvents()
