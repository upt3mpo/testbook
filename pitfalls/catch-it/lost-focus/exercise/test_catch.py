# YOUR TURN. Write a test that FAILS on the broken page and PASSES on the fixed page.
#
# Run it:  python3 -m pytest --exercises --show-red catch-it/lost-focus/exercise
# Hints are in ../exercise.md - try without them first.
import pytest


@pytest.mark.skip(reason="TODO: remove this marker once you have written the test")
def test_catches_the_lost_focus(page, open_pitfall):
    open_pitfall("catch-it/lost-focus")

    # TODO: open the post menu and choose Edit with the keyboard. Where is focus afterwards?

    assert False  # replace with a real assertion
