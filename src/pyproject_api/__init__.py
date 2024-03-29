"""PyProject API interface."""

from __future__ import annotations

from ._frontend import (
    BackendFailed,
    CmdStatus,
    EditableResult,
    Frontend,
    MetadataForBuildEditableResult,
    MetadataForBuildWheelResult,
    OptionalHooks,
    RequiresBuildEditableResult,
    RequiresBuildSdistResult,
    RequiresBuildWheelResult,
    SdistResult,
    WheelResult,
)
from ._version import version
from ._via_fresh_subprocess import SubprocessFrontend

#: semantic version of the project
__version__ = version

__all__ = [
    "BackendFailed",
    "CmdStatus",
    "EditableResult",
    "Frontend",
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
