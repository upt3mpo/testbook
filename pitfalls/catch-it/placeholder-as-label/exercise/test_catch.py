# YOUR TURN. Write a test that FAILS on the broken page and PASSES on the fixed page.
#
# Run it:  python3 -m pytest --exercises --show-red catch-it/placeholder-as-label/exercise
# Hints are in ../exercise.md - try without them first.
import pytest


@pytest.mark.skip(reason="TODO: remove this marker once you have written the test")
def test_catches_the_placeholder_only_fields(page, open_pitfall):
    open_pitfall("catch-it/placeholder-as-label")

    # TODO: find each field the way a screen reader user would meet it.

    assert False  # replace with a real assertion
