from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parent

CANVAS_PATH = (
    PROJECT_ROOT
    / "src"
    / "machine_builder"
    / "canvas.py"
)


def replace_once(
    text: str,
    pattern: str,
    replacement: str,
    description: str,
) -> str:
    """Replace exactly one regex match."""
    new_text, count = re.subn(
        pattern,
        replacement,
        text,
        count=1,
        flags=re.MULTILINE | re.DOTALL,
    )

    if count != 1:
        raise RuntimeError(
            f"{description}: expected exactly one match, "
            f"found {count}."
        )

    return new_text


def main() -> None:
    """Finish wiring the physical-endpoint connection model into canvas.py."""
    original = CANVAS_PATH.read_text(
        encoding="utf-8"
    )

    canvas = original

    # ---------------------------------------------------------------
    # 1. Replace the connection creation in _finish_connection_drag.
    #
    # The user may start at either end. We test the dragged orientation
    # first, then the reverse orientation. The stored connection itself
    # remains physically unordered.
    # ---------------------------------------------------------------

    old_finish_block = r"""        if \(
            source_port is not None
            and target_port is not None
        \):
            result = check_port_compatibility\(
                source_port,
                target_port,
            \)
            if result == CompatibilityResult\.COMPATIBLE:
                existing = any\(
                    connection\.source_port_id
                    == source_port\.id
                    and connection\.target_port_id
                    == target_port\.id
                    for connection
                    in self\.store\.model\.connections\.values\(\)
                \)
                if not existing:
                    connection_id = \(
                        f"connection-"
                        f"\{len\(self\.store\.model\.connections\) \+ 1\}"
                    \)
                    self\.store\.commit\(
                        CreateConnection\(
                            connection_id=connection_id,
                            source_port_id=source_port\.id,
                            target_port_id=target_port\.id,
                            connection_type=source_port\.port_type,
                        \)
                    \)
                    self\.statusBar\(\)\.showMessage\(
                        f"Connected: "
                        f"\{source_port\.label\} → "
                        f"\{target_port\.label\}"
                    \)

                else:
                    self\.statusBar\(\)\.showMessage\(
                        "That connection already exists\."
                    \)
            elif result == CompatibilityResult\.UNKNOWN:
                self\.statusBar\(\)\.showMessage\(
                    "Connection not committed: compatibility is unknown\."
                \)

            elif result == CompatibilityResult\.CONDITIONAL:
                self\.statusBar\(\)\.showMessage\(
                    "Connection not committed: compatibility is conditional\."
                \)
            else:
                self\.statusBar\(\)\.showMessage\(
                    "Connection rejected: incompatible ports\."
                \)

        else:
            self\.statusBar\(\)\.showMessage\(
                "Connection cancelled\."
            \)
"""

    new_finish_block = """        if (
            source_port is not None
            and target_port is not None
        ):
            # A physical connection has no direction. The compatibility
            # check may still need to know which port produces a signal and
            # which consumes it, so test both possible semantic orientations.
            result = check_port_compatibility(
                source_port,
                target_port,
            )

            semantic_source = source_port
            semantic_target = target_port

            if result != CompatibilityResult.COMPATIBLE:
                reverse_result = check_port_compatibility(
                    target_port,
                    source_port,
                )

                if (
                    reverse_result
                    == CompatibilityResult.COMPATIBLE
                ):
                    result = reverse_result
                    semantic_source = target_port
                    semantic_target = source_port

            if result == CompatibilityResult.COMPATIBLE:
                endpoint_a_id = source_port.id
                endpoint_b_id = target_port.id

                existing = any(
                    {
                        connection.endpoint_a_id,
                        connection.endpoint_b_id,
                    }
                    == {
                        endpoint_a_id,
                        endpoint_b_id,
                    }
                    for connection
                    in self.store.model.connections.values()
                )

                if not existing:
                    connection_id = (
                        f"connection-"
                        f"{len(self.store.model.connections) + 1}"
                    )

                    self.store.commit(
                        CreateConnection(
                            connection_id=connection_id,
                            endpoint_a_id=endpoint_a_id,
                            endpoint_b_id=endpoint_b_id,
                            connection_type=semantic_source.port_type,
                        )
                    )

                    self.statusBar().showMessage(
                        f"Connected: "
                        f"{semantic_source.label} → "
                        f"{semantic_target.label}"
                    )

                else:
                    self.statusBar().showMessage(
                        "That connection already exists."
                    )

            elif result == CompatibilityResult.UNKNOWN:
                self.statusBar().showMessage(
                    "Connection not committed: compatibility is unknown."
                )

            elif result == CompatibilityResult.CONDITIONAL:
                self.statusBar().showMessage(
                    "Connection not committed: compatibility is conditional."
                )

            else:
                self.statusBar().showMessage(
                    "Connection rejected: incompatible ports."
                )

        else:
            self.statusBar().showMessage(
                "Connection cancelled."
            )
"""

    canvas = replace_once(
        canvas,
        old_finish_block,
        new_finish_block,
        "physical connection commit block",
    )

    # ---------------------------------------------------------------
    # 2. Update stored-connection rendering.
    # ---------------------------------------------------------------

    old_render_block = r"""            source_item = \(
                self\._find_port_graphics_item\(
                    connection\.source_port_id
                \)
            \)

            target_item = \(
                self\._find_port_graphics_item\(
                    connection\.target_port_id
                \)
            \)
"""

    new_render_block = """            endpoint_a_item = (
                self._find_port_graphics_item(
                    connection.endpoint_a_id
                )
            )

            endpoint_b_item = (
                self._find_port_graphics_item(
                    connection.endpoint_b_id
                )
            )
"""

    canvas = replace_once(
        canvas,
        old_render_block,
        new_render_block,
        "stored connection endpoint lookup",
    )

    old_render_check = """            if (
                source_item is None
                or target_item is None
            ):
                continue
            start = source_item.scenePos()
            end = target_item.scenePos()
"""

    new_render_check = """            if (
                endpoint_a_item is None
                or endpoint_b_item is None
            ):
                continue

            start = endpoint_a_item.scenePos()
            end = endpoint_b_item.scenePos()
"""

    canvas = replace_once(
        canvas,
        old_render_check,
        new_render_check,
        "stored connection endpoint rendering",
    )

    # ---------------------------------------------------------------
    # Safety check.
    # ---------------------------------------------------------------

    if canvas == original:
        raise RuntimeError(
            "No changes were made."
        )

    CANVAS_PATH.write_text(
        canvas,
        encoding="utf-8",
    )

    print(
        "Physical endpoint connection model integrated into canvas.py."
    )


if __name__ == "__main__":
    main()