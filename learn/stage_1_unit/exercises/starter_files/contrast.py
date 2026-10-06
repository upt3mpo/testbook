"""WCAG colour contrast, as a small pure function.

The contrast ratio decides whether text is readable against its background. WCAG 2.2 success
criterion 1.4.3 requires 4.5:1 for normal text and 3:1 for large text.

Formulas are from the WCAG definitions of "relative luminance" and "contrast ratio":
  https://www.w3.org/TR/WCAG22/#dfn-relative-luminance
  https://www.w3.org/TR/WCAG22/#dfn-contrast-ratio

This is the Python twin of frontend/src/tests/helpers/contrast.js. It is the subject of the
accessibility step in Lab 2: copy it to backend/contrast.py and write the tests.
"""

import re

_HEX = re.compile(r"^#?([0-9a-f]{3}|[0-9a-f]{6})$", re.IGNORECASE)


def hex_to_rgb(hex_colour: str) -> tuple[int, int, int]:
    """Convert "#rgb" or "#rrggbb" (the # is optional) to (r, g, b), each 0-255."""
    match = _HEX.match(str(hex_colour).strip())
    if not match:
        raise ValueError(f"Invalid hex colour: {hex_colour!r}")
    digits = match.group(1)
    if len(digits) == 3:
        digits = "".join(d + d for d in digits)
    return tuple(int(digits[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _linearise(channel: int) -> float:
    """One sRGB channel (0-255) to its linear-light value, per the WCAG definition."""
    c = channel / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_colour: str) -> float:
    """Relative luminance: 0 for black, 1 for white."""
    r, g, b = (_linearise(c) for c in hex_to_rgb(hex_colour))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(colour_a: str, colour_b: str) -> float:
    """Contrast ratio between two colours, from 1 (identical) to 21 (black on white)."""
    lighter, darker = sorted(
        (relative_luminance(colour_a), relative_luminance(colour_b)), reverse=True
    )
    return (lighter + 0.05) / (darker + 0.05)


def passes_aa(foreground: str, background: str, large_text: bool = False) -> bool:
    """Does the pair meet WCAG AA? The ratio is NOT rounded: WCAG treats 4.499 as a fail.

    Large text (18pt, or 14pt bold) only needs 3:1.
    """
    return contrast_ratio(foreground, background) >= (3.0 if large_text else 4.5)
