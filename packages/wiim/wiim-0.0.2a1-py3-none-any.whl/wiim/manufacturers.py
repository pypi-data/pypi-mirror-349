"""Manufacturers and their devices for the LinkPlay component."""

from typing import Final


MANUFACTURER_WIIM: Final[str] = "Linkplay"
MODELS_WIIM_AMP: Final[str] = "WiiM Amp"
MODELS_WIIM_MINI: Final[str] = "WiiM Mini"
MODELS_WIIM_PRO: Final[str] = "WiiM Pro"
MODELS_GENERIC: Final[str] = "WiiM"

PROJECTID_LOOKUP: Final[dict[str, tuple[str, str]]] = {
    "WiiM_Amp_4layer": (MANUFACTURER_WIIM, MODELS_WIIM_AMP),
    "WiiM_Pro_with_gc4a": (MANUFACTURER_WIIM, MODELS_WIIM_PRO),
    "Muzo_Mini": (MANUFACTURER_WIIM, MODELS_WIIM_MINI),
}


def get_info_from_project(project: str) -> tuple[str, str]:
    """Get manufacturer and model info based on given project."""
    return PROJECTID_LOOKUP.get(project, (MANUFACTURER_WIIM, MODELS_GENERIC))
