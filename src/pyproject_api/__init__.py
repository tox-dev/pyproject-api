"""PyProject API interface."""

from __future__ import annotations

from ._frontend import (
    BackendFailed,
    BuiltMetadata,
    CmdStatus,
    EditableResult,
    Frontend,
    FrontendArgs,
    MetadataForBuildEditableResult,
    MetadataForBuildWheelResult,
    OptionalHooks,
    RequiresBuildEditableResult,
    RequiresBuildSdistResult,
    RequiresBuildWheelResult,
    SdistResult,
    WheelResult,
)
from ._version import __version__
from ._version import version as version
from ._via_fresh_subprocess import SubprocessFrontend

__all__ = [
    "BackendFailed",
    "BuiltMetadata",
    "CmdStatus",
    "EditableResult",
    "Frontend",
    "FrontendArgs",
    "MetadataForBuildEditableResult",
    "MetadataForBuildWheelResult",
    "OptionalHooks",
    "RequiresBuildEditableResult",
    "RequiresBuildSdistResult",
    "RequiresBuildWheelResult",
    "SdistResult",
    "SubprocessFrontend",
    "WheelResult",
    "__version__",
]
