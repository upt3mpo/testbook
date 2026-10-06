# YOUR TURN. Write a test that FAILS on the broken page and PASSES on the fixed page.
#
# Run it:  python3 -m pytest --exercises --show-red catch-it/silent-error/exercise
# Hints are in ../exercise.md - try without them first.
import pytest


@pytest.mark.skip(reason="TODO: remove this marker once you have written the test")
def test_catches_the_silent_error(page, open_pitfall):
    open_pitfall("catch-it/silent-error")
    page.get_by_role("button", name="Log in").click()

    # TODO: a sighted user sees the message appear. What would a screen reader user get,
    # and where is keyboard focus afterwards?

    assert False  # replace with a real assertion
