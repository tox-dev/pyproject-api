"""PyProject API interface."""

from __future__ import annotations

__lazy_modules__ = [
    f"{__spec__.parent}._frontend",  # ty: ignore[unresolved-attribute]  # imported modules have a spec
    f"{__spec__.parent}._version",  # ty: ignore[unresolved-attribute]  # imported modules have a spec
    f"{__spec__.parent}._via_fresh_subprocess",  # ty: ignore[unresolved-attribute]  # imported modules have a spec
]

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
from ._version import __version__
from ._version import version as version
from ._via_fresh_subprocess import SubprocessFrontend

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
