# YOUR TURN. The suspect test is green on a page where the menu button's only name is a symbol.
# 1. Prove it: what could you remove from the page and the test would still pass?
# 2. Write a version you CAN trust: it must fail on the broken page and pass on the fixed one.
#
# Run it:  python3 -m pytest --exercises --show-red trust-it/test-id-hides-bug/exercise
# Hints are in ../exercise.md - try without them first.
import pytest


@pytest.mark.skip(reason="TODO: remove this marker once you have written the test")
def test_a_trustworthy_post_menu_test(page, open_pitfall):
    open_pitfall("trust-it/test-id-hides-bug")

    # TODO: find the button the way a user would, not the way a developer labelled it.

    assert False  # replace with a real assertion
