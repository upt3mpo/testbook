# YOUR TURN. Write a test that FAILS on the broken page and PASSES on the fixed page.
#
# Run it:  python3 -m pytest --exercises --show-red catch-it/dark-mode-contrast/exercise
# Hints are in ../exercise.md - try without them first.
import pytest


@pytest.mark.skip(reason="TODO: remove this marker once you have written the test")
def test_catches_the_dark_mode_contrast_failure(page, open_pitfall):
    open_pitfall("catch-it/dark-mode-contrast")

    # TODO: a default scan of this page is green. What state have you not looked at yet?

    assert False  # replace with a real assertion
