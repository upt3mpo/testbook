# YOUR TURN. Write a test that FAILS on the broken page and PASSES on the fixed page.
#
# Run it:  python3 -m pytest --exercises --show-red catch-it/nested-interactive/exercise
# Hints are in ../exercise.md - try without them first.
import pytest


@pytest.mark.skip(reason="TODO: remove this marker once you have written the test")
def test_catches_the_nested_interactive_control(page, open_pitfall):
    open_pitfall("catch-it/nested-interactive")

    # TODO: a keyboard user meets this control by pressing Tab. How many times do they have
    # to press it to get past the "View" control?

    assert False  # replace with a real assertion
