"""Reference solution for Lab 2, accessibility step (Python track).

Copy stage_1_unit/exercises/starter_files/contrast.py to backend/contrast.py first. Then put
this file at backend/tests/test_contrast_lab.py and run:

    cd backend && pytest tests/test_contrast_lab.py -v

The last class is the optional Step 7 challenge: it reads Testbook's real design tokens from
frontend/src/index.css and checks every text/background pair in both themes.
"""

import re
from pathlib import Path

import pytest
from contrast import contrast_ratio, hex_to_rgb, passes_aa, relative_luminance


class TestHexToRgb:
    def test_reads_six_digit_and_three_digit_hex_with_or_without_hash(self):
        assert hex_to_rgb("#1264d0") == (18, 100, 208)
        assert hex_to_rgb("fff") == (255, 255, 255)
        assert hex_to_rgb("#0a0") == (0, 170, 0)

    @pytest.mark.parametrize("bad", ["", "#12", "#12345", "blue", "#gggggg", None])
    def test_rejects_invalid_input(self, bad):
        with pytest.raises(ValueError, match="Invalid hex colour"):
            hex_to_rgb(bad)


class TestRelativeLuminance:
    def test_is_zero_for_black_and_one_for_white(self):
        assert relative_luminance("#000000") == 0
        assert relative_luminance("#ffffff") == pytest.approx(1)


class TestContrastRatio:
    def test_black_on_white_is_21_and_a_colour_on_itself_is_1(self):
        assert contrast_ratio("#000000", "#ffffff") == pytest.approx(21, abs=1e-5)
        assert contrast_ratio("#2d88ff", "#2d88ff") == pytest.approx(1)

    def test_does_not_depend_on_which_colour_is_the_foreground(self):
        assert contrast_ratio("#1264d0", "#ffffff") == contrast_ratio("#ffffff", "#1264d0")

    # Real Testbook colours. The first two are the dark-theme bug (A11Y-016) and its fix.
    @pytest.mark.parametrize(
        ("foreground", "background", "expected"),
        [
            ("#ffffff", "#2d88ff", 3.46),
            ("#ffffff", "#1668d9", 5.23),
            ("#ffffff", "#1264d0", 5.59),
            ("#d32f2f", "#18191a", 3.54),
        ],
    )
    def test_real_testbook_colours(self, foreground, background, expected):
        # approx(abs=0.005) compares to two decimal places. Never compare floats with ==.
        assert contrast_ratio(foreground, background) == pytest.approx(expected, abs=0.005)


class TestPassesAA:
    def test_boundary_767676_passes_and_777777_fails_though_they_look_identical(self):
        assert passes_aa("#767676", "#ffffff") is True  # 4.54:1
        assert passes_aa("#777777", "#ffffff") is False  # 4.48:1

    def test_the_ratio_is_not_rounded(self):
        ratio = contrast_ratio("#777777", "#ffffff")
        assert 4.4 < ratio < 4.5

    def test_large_text_only_needs_3_to_1(self):
        # 3.46:1 fails for normal text and passes for large text.
        assert passes_aa("#ffffff", "#2d88ff") is False
        assert passes_aa("#ffffff", "#2d88ff", large_text=True) is True


# ---- Step 7 (optional challenge): check the real design tokens -----------------------------

CSS = Path(__file__).resolve().parents[2] / "frontend" / "src" / "index.css"
TOKEN = re.compile(r"(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{3,6})\b")


def read_block(css: str, selector: str) -> dict[str, str]:
    block = re.search(re.escape(selector) + r"\s*\{([^}]*)\}", css)
    assert block, f"No {selector} block found"
    return dict(TOKEN.findall(block.group(1)))


def theme_tokens() -> dict[str, dict[str, str]]:
    css = CSS.read_text(encoding="utf-8")
    light = read_block(css, ":root")
    return {"light": light, "dark": {**light, **read_block(css, "[data-theme='dark']")}}


PAIRS = [
    ("--text-primary", "--bg-primary"),
    ("--text-primary", "--bg-secondary"),
    ("--text-secondary", "--bg-primary"),
    ("--text-secondary", "--bg-secondary"),
    ("--accent-color", "--bg-primary"),
    ("#ffffff", "--accent-fill"),
    ("--error-text", "--bg-primary"),
]


@pytest.mark.parametrize("theme", ["light", "dark"])
@pytest.mark.parametrize(("foreground", "background"), PAIRS)
def test_design_token_pair_meets_aa(theme, foreground, background):
    tokens = theme_tokens()[theme]
    fg = tokens.get(foreground, foreground)
    bg = tokens.get(background, background)
    ratio = contrast_ratio(fg, bg)
    assert ratio >= 4.5, f"{foreground} ({fg}) on {background} ({bg}) is {ratio:.2f}:1 in {theme}"
