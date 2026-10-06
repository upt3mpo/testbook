# YOUR TURN. Write a test that FAILS on the broken page and PASSES on the fixed page.
#
# Run it:  python3 -m pytest --exercises --show-red catch-it/invisible-tab-stops/exercise
# Hints are in ../exercise.md - try without them first.
import pytest


@pytest.mark.skip(reason="TODO: remove this marker once you have written the test")
def test_catches_the_invisible_tab_stops(page, open_pitfall):
    open_pitfall("catch-it/invisible-tab-stops")

    # TODO: press Tab through the page and decide, at each stop, whether a person
    # looking at the screen could see the control that has focus.

    assert False  # replace with a real assertion
