"""Durable JSON persistence for Machine Structure Editor state.

Persistence is intentionally separate from:
- the canonical semantic model
- visual presentation classes
- mutations
- the application store

The persisted unit is the complete EditorState:
    visual model + canonical semantic model

The file format is JSON so project files remain inspectable and versionable.
"""

from __future__ import annotations

import json
import os
from dataclasses import fields, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any, TypeAlias

from .controller import Controller
from .controller_resource import ControllerResource
from .controller_resource_assignment import (
    ControllerResourceAssignment,
)
from .editor_state import EditorState
from .semantic_capability import Capability
from .semantic_connection import SemanticConnection
from .semantic_model import (
    CanonicalMachineModel,
    Function,
    HardwareDefinition,
    Machine,
    MachineComponent,
    Provenance,
    SemanticPort,
)
from .semantic_relationship import SemanticRelationship
from .semantic_value import (
    SemanticValue,
    SemanticValueStatus,
)
from .visual_model import (
    VisualConnection,
    VisualGroup,
    VisualModel,
    VisualNode,
    VisualPort,
    VisualView,
)


FORMAT_NAME = "machine-builder-editor"
FORMAT_VERSION = 1


PersistableType: TypeAlias = type[Any]


_TYPE_REGISTRY: dict[str, PersistableType] = {
    cls.__module__ + "." + cls.__qualname__: cls
    for cls in (
        Provenance,
        HardwareDefinition,
        SemanticPort,
        Function,
        MachineComponent,
        Machine,
        Capability,
        Controller,
        ControllerResource,
        ControllerResourceAssignment,
        SemanticConnection,
        SemanticRelationship,
        SemanticValue,
        SemanticValueStatus,
        VisualPort,
        VisualNode,
        VisualConnection,
        VisualGroup,
        VisualView,
        VisualModel,
        CanonicalMachineModel,
        EditorState,
    )
}


def _type_name(value: type[Any]) -> str:
    return value.__module__ + "." + value.__qualname__


def _encode(value: Any) -> Any:
    """Convert supported model values to JSON-compatible structures."""
    if value is None:
        return None

    if isinstance(value, Enum):
        type_name = _type_name(type(value))

        if type_name not in _TYPE_REGISTRY:
            raise TypeError(
                f"Unsupported enum type for persistence: {type_name}"
            )

        return {
            "__enum__": type_name,
            "value": value.value,
        }

    if is_dataclass(value):
        type_name = _type_name(type(value))

        if type_name not in _TYPE_REGISTRY:
            raise TypeError(
                f"Unsupported dataclass type for persistence: {type_name}"
            )

        return {
            "__type__": type_name,
            "fields": {
                field.name: _encode(
                    getattr(
                        value,
                        field.name,
                    )
                )
                for field in fields(value)
            },
        }

    if isinstance(value, dict):
        encoded: dict[str, Any] = {}

        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError(
                    "Persistence currently requires string dictionary keys."
                )

            encoded[key] = _encode(item)

        return {
            "__dict__": encoded,
        }

    if isinstance(value, list):
        return {
            "__list__": [
                _encode(item)
                for item in value
            ],
        }

    if isinstance(value, tuple):
        return {
            "__tuple__": [
                _encode(item)
                for item in value
            ],
        }

    if isinstance(value, (str, int, float, bool)):
        return value

    raise TypeError(
        "Unsupported value for persistence: "
        f"{type(value).__module__}.{type(value).__qualname__}"
    )


def _decode(value: Any) -> Any:
    """Reconstruct supported model values from JSON-compatible data."""
    if value is None:
        return None

    if isinstance(value, (str, int, float, bool)):
        return value

    if not isinstance(value, dict):
        raise ValueError(
            "Invalid persisted value."
        )

    if "__enum__" in value:
        type_name = value.get(
            "__enum__"
        )

        if not isinstance(type_name, str):
            raise ValueError(
                "Persisted enum type must be a string."
            )

        enum_type = _TYPE_REGISTRY.get(
            type_name
        )

        if enum_type is None:
            raise ValueError(
                f"Unsupported persisted enum type: {type_name}"
            )

        if not issubclass(
            enum_type,
            Enum,
        ):
            raise ValueError(
                f"Persisted type is not an enum: {type_name}"
            )

        return enum_type(
            value["value"]
        )

    if "__dict__" in value:
        encoded_items = value["__dict__"]

        if not isinstance(
            encoded_items,
            dict,
        ):
            raise ValueError(
                "Persisted dictionary payload is invalid."
            )

        return {
            key: _decode(item)
            for key, item in encoded_items.items()
        }

    if "__list__" in value:
        encoded_items = value["__list__"]

        if not isinstance(
            encoded_items,
            list,
        ):
            raise ValueError(
                "Persisted list payload is invalid."
            )

        return [
            _decode(item)
            for item in encoded_items
        ]

    if "__tuple__" in value:
        encoded_items = value["__tuple__"]

        if not isinstance(
            encoded_items,
            list,
        ):
            raise ValueError(
                "Persisted tuple payload is invalid."
            )

        return tuple(
            _decode(item)
            for item in encoded_items
        )

    if "__type__" in value:
        type_name = value.get(
            "__type__"
        )

        if not isinstance(type_name, str):
            raise ValueError(
                "Persisted dataclass type must be a string."
            )

        dataclass_type = _TYPE_REGISTRY.get(
            type_name
        )

        if dataclass_type is None:
            raise ValueError(
                f"Unsupported persisted dataclass type: {type_name}"
            )

        fields_payload = value.get(
            "fields"
        )

        if not isinstance(
            fields_payload,
            dict,
        ):
            raise ValueError(
                f"Invalid field payload for: {type_name}"
            )

        decoded_fields = {
            name: _decode(item)
            for name, item in fields_payload.items()
        }

        return dataclass_type(
            **decoded_fields
        )

    raise ValueError(
        "Persisted object has no recognized type marker."
    )


def serialize_editor_state(
    state: EditorState,
) -> dict[str, Any]:
    """Serialize complete editor state into a JSON-ready document."""
    encoded_state = _encode(
        state
    )

    return {
        "format": FORMAT_NAME,
        "format_version": FORMAT_VERSION,
        "state": encoded_state,
    }


def deserialize_editor_state(
    document: dict[str, Any],
) -> EditorState:
    """Deserialize a persistence document into complete editor state."""
    if document.get(
        "format"
    ) != FORMAT_NAME:
        raise ValueError(
            "Unsupported Machine Builder persistence format."
        )

    version = document.get(
        "format_version"
    )

    if version != FORMAT_VERSION:
        raise ValueError(
            "Unsupported Machine Builder persistence version: "
            f"{version}"
        )

    if "state" not in document:
        raise ValueError(
            "Persistence document does not contain editor state."
        )

    state = _decode(
        document["state"]
    )

    if not isinstance(
        state,
        EditorState,
    ):
        raise ValueError(
            "Persistence document did not contain an EditorState."
        )

    return state


def save_editor_state(
    state: EditorState,
    path: str | Path,
) -> None:
    """Save complete editor state as formatted UTF-8 JSON.

    The file is written to a temporary sibling first and then replaced so
    an interrupted write does not intentionally destroy the previous file.
    """
    destination = Path(
        path
    )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    document = serialize_editor_state(
        state
    )

    text = json.dumps(
        document,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
    )

    temporary = destination.with_name(
        destination.name + ".tmp"
    )

    try:
        temporary.write_text(
            text + "\n",
            encoding="utf-8",
        )

        os.replace(
            temporary,
            destination,
        )
    finally:
        if temporary.exists():
            temporary.unlink()


def load_editor_state(
    path: str | Path,
) -> EditorState:
    """Load complete editor state from a JSON project file."""
    source = Path(
        path
    )

    text = source.read_text(
        encoding="utf-8"
    )

    try:
        document = json.loads(
            text
        )
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid Machine Builder JSON file: {source}"
        ) from exc

    if not isinstance(
        document,
        dict,
    ):
        raise ValueError(
            "Machine Builder persistence root must be a JSON object."
        )

    return deserialize_editor_state(
        document
    )