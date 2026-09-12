from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parent

CANVAS_PATH = (
    PROJECT_ROOT
    / "src"
    / "machine_builder"
    / "canvas.py"
)


def replace_required(
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
    """Add direct selection and deletion of visual connections."""
    original = CANVAS_PATH.read_text(
        encoding="utf-8"
    )

    canvas_text = original

    # ---------------------------------------------------------------
    # 1. Add DeleteConnection to the mutation imports.
    # ---------------------------------------------------------------

    canvas_text = replace_required(
        canvas_text,
        r"from \.mutations import \(\n"
        r"    CreateConnection,\n"
        r"    CreateNode,\n"
        r"    DeleteNodes,\n"
        r"    MoveNodes,\n"
        r"\)",
        """from .mutations import (
    CreateConnection,
    CreateNode,
    DeleteConnection,
    DeleteNodes,
    MoveNodes,
)""",
        "mutation imports",
    )

    # ---------------------------------------------------------------
    # 2. Pass the connection-selection callback when creating a wire.
    # ---------------------------------------------------------------

    canvas_text = replace_required(
        canvas_text,
        r"graphics = ConnectionGraphicsItem\(\n"
        r"\s+connection\n"
        r"\s+\)",
        """graphics = ConnectionGraphicsItem(
                        connection=connection,
                        selection_callback=self._connection_selected,
                    )""",
        "connection graphics creation",
    )

    # ---------------------------------------------------------------
    # 3. Replace _delete_selected() by locating the next method.
    # ---------------------------------------------------------------

    canvas_text = replace_required(
        canvas_text,
        r"    def _delete_selected\(\n"
        r"        self,\n"
        r"    \) -> None:\n"
        r".*?"
        r"    def _focus_node\(",
        """    def _delete_selected(
        self,
    ) -> None:
        \"\"\"Delete selected connections or nodes as one user action.\"\"\"
        selected_connections = tuple(
            item.connection_id
            for item in self.scene.selectedItems()
            if isinstance(
                item,
                ConnectionGraphicsItem,
            )
        )

        if selected_connections:
            for connection_id in selected_connections:
                self.store.commit(
                    DeleteConnection(
                        connection_id=connection_id
                    )
                )

            self.statusBar().showMessage(
                f\"Deleted {len(selected_connections)} connection\"
                + (
                    \"\"
                    if len(selected_connections) == 1
                    else \"s\"
                )
            )

            return

        selected_ids = tuple(
            item.node_id
            for item in self.scene.selectedItems()
            if isinstance(
                item,
                NodeGraphicsItem,
            )
        )

        if not selected_ids:
            return

        self.store.commit(
            DeleteNodes(
                node_ids=selected_ids
            )
        )

        self.statusBar().showMessage(
            f\"Deleted {len(selected_ids)} node\"
            + (
                \"\"
                if len(selected_ids) == 1
                else \"s\"
            )
        )

    def _focus_node(""",
        "delete method",
    )

    # ---------------------------------------------------------------
    # 4. Insert the connection-selection callback immediately before
    #    _focus_node().
    # ---------------------------------------------------------------

    connection_callback = """    def _connection_selected(
        self,
        connection_id: str,
        selected: bool,
    ) -> None:
        \"\"\"Show status information when a connection is selected.\"\"\"
        if not selected:
            return

        connection = (
            self.store.model.connections.get(
                connection_id
            )
        )

        if connection is None:
            return

        source = self.store.model.find_port(
            connection.source_port_id
        )

        target = self.store.model.find_port(
            connection.target_port_id
        )

        if source is None or target is None:
            self.statusBar().showMessage(
                "Selected connection"
            )
            return

        self.statusBar().showMessage(
            f"Selected connection: "
            f"{source.label} ↔ {target.label}"
        )

"""

    canvas_text = replace_required(
        canvas_text,
        r"    def _focus_node\(",
        connection_callback
        + "    def _focus_node(",
        "connection selection callback insertion",
    )

    # ---------------------------------------------------------------
    # Safety check:
    # Do not write anything unless all expected changes happened.
    # ---------------------------------------------------------------

    if canvas_text == original:
        raise RuntimeError(
            "No changes were made."
        )

    CANVAS_PATH.write_text(
        canvas_text,
        encoding="utf-8",
    )

    print(
        "Connection selection and deletion support added."
    )
    print(
        f"Updated: {CANVAS_PATH}"
    )


if __name__ == "__main__":
    main()