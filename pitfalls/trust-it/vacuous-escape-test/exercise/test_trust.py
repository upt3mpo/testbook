# YOUR TURN. The suspect test is green on a page where Escape does nothing.
# 1. Prove it: which line of the page can you delete and the test still passes?
# 2. Write a version that you CAN trust: it must fail on the broken page and pass on the
#    fixed page.
#
# Run it:  python3 -m pytest --exercises --show-red trust-it/vacuous-escape-test/exercise
# Hints are in ../exercise.md - try without them first.
import pytest


@pytest.mark.skip(reason="TODO: remove this marker once you have written the test")
def test_a_trustworthy_escape_test(page, open_pitfall):
    open_pitfall("trust-it/vacuous-escape-test")

    # TODO: make sure the menu is really open before you press Escape.

    assert False  # replace with a real assertion
