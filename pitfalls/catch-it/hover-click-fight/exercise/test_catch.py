# YOUR TURN. Write a test that FAILS on the broken page and PASSES on the fixed page.
#
# Run it:  python3 -m pytest --exercises --show-red catch-it/hover-click-fight/exercise
# Hints are in ../exercise.md - try without them first.
import pytest


@pytest.mark.skip(reason="TODO: remove this marker once you have written the test")
def test_catches_the_hover_click_fight(page, open_pitfall):
    open_pitfall("catch-it/hover-click-fight")

    # TODO: open the picker the way a real mouse user does, then check that what the
    # screen shows and what assistive technology is told (aria-expanded) agree.

    assert False  # replace with a real assertion
