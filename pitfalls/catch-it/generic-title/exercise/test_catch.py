# YOUR TURN. Write a test that FAILS on the broken page and PASSES on the fixed page.
#
# Run it:  python3 -m pytest --exercises --show-red catch-it/generic-title/exercise
# Hints are in ../exercise.md - try without them first.
import pytest


@pytest.mark.skip(reason="TODO: remove this marker once you have written the test")
def test_catches_the_generic_title(page, open_pitfall):
    open_pitfall("catch-it/generic-title")
    page.get_by_role("link", name="Settings").click()

    # TODO: the content changed. What else should have changed with it?

    assert False  # replace with a real assertion
