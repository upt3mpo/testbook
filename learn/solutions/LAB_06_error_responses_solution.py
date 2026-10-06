"""Reference solution for Lab 6 (Python), Part 3 Step 3: errors are a user interface.

Put this file at backend/tests/integration/test_error_responses_lab.py and run:

    cd backend && pytest tests/integration/test_error_responses_lab.py -v

It uses the standard fixtures from backend/tests/conftest.py (client, test_user, auth_headers).
"""

import pytest

VALID_REGISTRATION = {
    "email": "zed@example.com",
    "username": "zed",
    "display_name": "Zed",
    "password": "Password1!",
}


def bad_requests(test_user):
    """Each case: (label, method, url, json body or None, needs auth)."""
    return [
        ("invalid email", "post", "/api/auth/register", {**VALID_REGISTRATION, "email": "a@b"}, False),
        ("missing fields", "post", "/api/auth/register", {"email": "x@y.com"}, False),
        ("duplicate email", "post", "/api/auth/register", {**VALID_REGISTRATION, "email": test_user.email}, False),
        ("wrong password", "post", "/api/auth/login", {"email": test_user.email, "password": "nope"}, False),
        ("unknown post", "get", "/api/posts/99999", None, True),
    ]


@pytest.fixture
def error_responses(client, test_user, auth_headers):
    """Make every bad request once and return {label: response}."""
    responses = {}
    for label, method, url, body, needs_auth in bad_requests(test_user):
        kwargs = {"headers": auth_headers} if needs_auth else {}
        if body is not None:
            kwargs["json"] = body
        responses[label] = getattr(client, method)(url, **kwargs)
    return responses


def test_every_error_is_a_4xx_with_a_json_detail(error_responses):
    for label, response in error_responses.items():
        assert 400 <= response.status_code < 500, f"{label}: got {response.status_code}"
        assert "detail" in response.json(), f"{label}: no 'detail' in the body"


def test_detail_is_always_one_of_two_shapes_the_frontend_handles(error_responses):
    """The shape contract. The real bug (A11Y-019) was a frontend that only expected a string."""
    for label, response in error_responses.items():
        detail = response.json()["detail"]
        if isinstance(detail, str):
            assert detail.strip(), f"{label}: empty message"
        else:
            assert isinstance(detail, list) and detail, f"{label}: unexpected shape {detail!r}"
            for issue in detail:
                assert isinstance(issue["msg"], str), f"{label}: issue has no text message"
                assert isinstance(issue["loc"], list), f"{label}: issue does not say where"


def test_the_two_shapes_really_do_both_occur(error_responses):
    """Why the frontend needs both branches: a 422 is a list, everything else here is a string."""
    assert isinstance(error_responses["invalid email"].json()["detail"], list)
    assert isinstance(error_responses["wrong password"].json()["detail"], str)


def test_messages_are_specific_not_generic(error_responses):
    generic = {"error", "bad request", "something went wrong", "failed", "invalid"}
    for label, response in error_responses.items():
        detail = response.json()["detail"]
        text = detail if isinstance(detail, str) else " ".join(issue["msg"] for issue in detail)
        assert text.strip().lower() not in generic, f"{label}: '{text}' tells the user nothing"
        assert len(text) > 10, f"{label}: '{text}' is too short to be useful"


def test_validation_errors_say_which_field(error_responses):
    """WCAG 3.3.1 Error Identification: the user has to know WHAT to fix."""
    issues = error_responses["missing fields"].json()["detail"]
    fields = {issue["loc"][-1] for issue in issues}
    assert {"username", "display_name", "password"} <= fields

    assert "email" in str(error_responses["invalid email"].json()["detail"][0]["loc"])
    assert "email" in error_responses["duplicate email"].json()["detail"].lower()


def test_login_failure_does_not_reveal_which_part_was_wrong(client, test_user):
    """Clear enough to act on, vague enough not to help an attacker find valid emails."""
    wrong_password = client.post("/api/auth/login", json={"email": test_user.email, "password": "nope"})
    unknown_email = client.post("/api/auth/login", json={"email": "nobody@example.com", "password": "nope"})

    assert wrong_password.status_code == unknown_email.status_code == 401
    assert wrong_password.json()["detail"] == unknown_email.json()["detail"]


def test_errors_do_not_leak_internals(error_responses):
    forbidden = ["traceback", "sqlalchemy", 'file "', "internal server error", "select "]
    for label, response in error_responses.items():
        body = response.text.lower()
        assert not any(word in body for word in forbidden), f"{label} leaks an internal detail"


# ---- Challenge: find a gap -----------------------------------------------------------------
# The API accepts an empty post and a very long username. Document the gap you found with a test
# that states what SHOULD happen, marked xfail(strict=True) so it turns red the day it is fixed.


@pytest.mark.xfail(strict=True, reason="The API currently accepts an empty post")
def test_an_empty_post_is_rejected_with_a_clear_message(client, auth_headers):
    response = client.post("/api/posts/", headers=auth_headers, json={"content": ""})
    assert response.status_code == 422
