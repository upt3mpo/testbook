"""
Placeholder tests for the OWASP Top 10 categories this suite does not cover.

tests/security/README.md documents three genuine gaps: A06 (Vulnerable and
Outdated Components), A08 (Software and Data Integrity Failures), and A09
(Security Logging and Monitoring Failures). Saying "not covered" in a table
is honest, but it doesn't show a student what testing those categories would
actually look like.

Every test below is skipped - none of them run as part of the suite, and
none of them affect the pass/fail count. Each one is a complete, runnable
sketch of what real coverage would require: the assertion it would make, why
it isn't wired up in this repo, how you'd wire it up, and how you'd actually
run it in production (which is often a different answer than "in this test
file"). Read the docstring, not just the skip reason.
"""

import pytest


class TestVulnerableAndOutdatedComponents:
    """A06:2021 - Vulnerable and Outdated Components."""

    @pytest.mark.skip(
        reason="Requires pip-audit and a network call to the PyPI advisory "
        "database - see the docstring for what this would check."
    )
    def test_backend_dependencies_have_no_known_cves(self):
        """
        What this test would do: Run pip-audit against backend/requirements.txt
        and assert it reports zero vulnerabilities at or above a severity
        threshold (e.g. "high" or above, so a low-severity advisory in a
        transitive dev dependency doesn't fail CI on every PR).

            result = subprocess.run(
                ["pip-audit", "-r", "backend/requirements.txt", "--format=json"],
                capture_output=True,
                text=True,
            )
            report = json.loads(result.stdout)
            high_severity = [
                v for pkg in report["dependencies"] for v in pkg.get("vulns", [])
                if v.get("severity", "").lower() in ("high", "critical")
            ]
            assert high_severity == [], f"Found high-severity CVEs: {high_severity}"

        Why it's skipped: pip-audit needs to reach PyPI's advisory database
        (or a pre-downloaded copy of it) over the network. This test suite
        runs against a local backend with no guarantee of outbound network
        access, and a flaky network call has no business being a required
        test in a suite students run repeatedly while learning.

        How you would implement it: pip install pip-audit, run it as shown
        above, and either fail the test on any high-or-above finding or
        write the JSON report to a file for a human to triage - the second
        option is usually better for a first pass, since a brand-new CVE in
        a widely-used package (e.g. a fastapi transitive dependency) can
        appear overnight and you don't want it silently blocking every PR
        the moment the advisory is published.

        What you would actually do in production: this belongs in its own
        scheduled CI job (`.github/dependabot.yml` already handles the
        "propose a version bump" half of this), not in the per-PR test run.
        Dependency vulnerabilities appear between code changes, on a
        schedule set by researchers finding them, not because someone
        opened a PR - running the check on every commit wastes CI minutes
        rediscovering the same finding.
        """

    @pytest.mark.skip(
        reason="Requires npm audit and a network call to the npm advisory "
        "registry - see the docstring for what this would check."
    )
    def test_frontend_dependencies_have_no_known_cves(self):
        """
        What this test would do: Run `npm audit --json` from frontend/ and
        assert there are no vulnerabilities at "high" severity or above,
        mirroring the backend check but for the frontend's npm dependency
        tree instead of pip's.

            result = subprocess.run(
                ["npm", "audit", "--json"],
                cwd="frontend",
                capture_output=True,
                text=True,
            )
            report = json.loads(result.stdout)
            high_or_above = report["metadata"]["vulnerabilities"]["high"] + \\
                report["metadata"]["vulnerabilities"]["critical"]
            assert high_or_above == 0, f"npm audit found {high_or_above} high/critical issues"

        Why it's skipped: same reason as the backend version - it needs to
        reach npm's registry over the network, and this repo's test suite
        is designed to run fully offline against a local backend once
        dependencies are installed.

        How you would implement it: the command above, run from a shell
        with network access. `npm audit fix` can auto-resolve some findings
        by bumping to a patched semver-compatible version, but that should
        be a deliberate step a maintainer reviews, not something a test
        does silently.

        What you would actually do in production: same answer as the
        backend case - a scheduled CI job, not a per-PR gate, backed by
        Dependabot's automatic PRs (`.github/dependabot.yml` already covers
        `/frontend` on the npm ecosystem) for the actual remediation.
        """


class TestSoftwareAndDataIntegrityFailures:
    """A08:2021 - Software and Data Integrity Failures."""

    @pytest.mark.skip(
        reason="Requires generating a hash-pinned requirements file with "
        "pip-compile and comparing it against the committed one - not set "
        "up in this repo yet."
    )
    def test_backend_dependencies_are_pinned_to_verifiable_hashes(self):
        """
        What this test would do: Assert that backend/requirements.txt pins
        every dependency to a specific version AND a cryptographic hash of
        the package contents, not just a version number. A version pin
        (fastapi==0.115.0) stops you from silently getting a *different*
        version; a hash pin stops you from silently getting a *tampered*
        artifact published under the *same* version number - which is
        exactly the class of attack A08 is about (a compromised package
        registry or a malicious mirror serving different bytes for the
        same version string).

            with open("backend/requirements.txt") as f:
                lines = [l for l in f if l.strip() and not l.startswith("#")]
            unhashed = [l for l in lines if "--hash=" not in l]
            assert unhashed == [], (
                f"{len(unhashed)} dependencies have no hash pin: {unhashed}"
            )

        Why it's skipped: this repo's requirements.txt is version-pinned
        (see the `==` pins throughout) but not hash-pinned, and generating
        hash-pinned output means switching the whole install workflow to
        `pip-compile --generate-hashes` + `pip install --require-hashes`,
        which is a real change to how every contributor installs the
        backend, not something to flip on inside a test file.

        How you would implement it: `pip install pip-tools`, then
        `pip-compile --generate-hashes requirements.in -o requirements.txt`
        to produce a hash-pinned file, and `pip install --require-hashes -r
        requirements.txt` to actually enforce it at install time (the
        enforcement has to happen at install, not just at test time - by
        the time a test runs, the possibly-tampered package is already
        imported).

        What you would actually do in production: adopt hash pinning
        repo-wide as an install-time gate, and pair it with Dependabot
        (already configured) so hash updates arrive as reviewable PRs
        alongside version bumps instead of as a wall of unreviewable hex.
        """

    @pytest.mark.skip(
        reason="Requires parsing every CI workflow file and checking each "
        "'uses:' reference against the commit-SHA-pinning convention - not "
        "implemented, and the repo does not currently follow that "
        "convention."
    )
    def test_ci_workflows_pin_actions_to_a_commit_sha(self):
        """
        What this test would do: Parse every `.github/workflows/*.yml` file
        and assert that each `uses:` step references a full commit SHA
        (e.g. `actions/checkout@8f4b7f8...`) rather than a mutable tag
        (e.g. `actions/checkout@v7`). A tag can be moved by whoever
        controls the action's repository to point at different code after
        you've already reviewed and trusted it - a SHA cannot. This is CI
        supply-chain integrity, the same category of risk as the
        dependency-hash test above, applied to the pipeline itself instead
        of the application's dependencies.

            import re, glob, yaml
            unpinned = []
            for path in glob.glob(".github/workflows/*.yml"):
                workflow = yaml.safe_load(open(path))
                for job in workflow.get("jobs", {}).values():
                    for step in job.get("steps", []):
                        ref = step.get("uses", "")
                        if ref and not re.search(r"@[0-9a-f]{40}$", ref):
                            unpinned.append(f"{path}: {ref}")
            assert unpinned == [], f"Actions pinned by tag, not SHA: {unpinned}"

        Why it's skipped: as of this pass, every workflow in this repo
        (`backend-tests.yml`, `frontend-tests.yml`, `e2e-tests.yml`, and
        others) pins actions by version tag - `actions/checkout@v7`,
        `actions/setup-python@v7`, `actions/upload-artifact@v7` - not by
        SHA. Writing this test to run (rather than skip) today would mean
        it fails immediately on every one of those lines, which is a real
        finding worth acting on, just not inside this PR's scope.

        How you would implement it: pick a pinning tool (GitHub's own
        dependabot.yml can auto-update pinned SHAs the same way it updates
        version tags, so this doesn't have to mean losing update
        automation) and repoint every `uses:` line at the SHA matching its
        current tag, e.g. `actions/checkout@8f4b7f84864484a7bf31766abe9204da3cbe65b3  # v7`
        with the tag kept as a trailing comment for human readability.

        What you would actually do in production: treat this as a one-time
        repo-wide edit plus a lint rule (this test, made non-skipped) that
        keeps it true going forward, rather than something to fix
        opportunistically one workflow at a time.
        """


class TestSecurityLoggingAndMonitoringFailures:
    """A09:2021 - Security Logging and Monitoring Failures."""

    @pytest.mark.skip(
        reason="backend/logger.py exists but is not wired into auth.py - "
        "there is nothing for this test to assert against yet."
    )
    def test_failed_login_attempts_are_logged(self, api_client):
        """
        What this test would do: Attempt a login with a wrong password,
        then assert that a security-relevant log entry was actually
        produced for it - in a real system, by querying whatever log
        aggregation the deployment uses (structured JSON logs shipped to a
        log store, most commonly); in a test environment without one, by
        capturing the backend's log output directly.

            import logging
            with caplog.at_level(logging.WARNING, logger="testbook.auth"):
                api_client.post(f"{BASE_URL}/auth/login", json={
                    "email": "sarah.johnson@testbook.com",
                    "password": "WrongPassword123!",
                })
            assert any(
                "failed login" in record.message.lower()
                for record in caplog.records
            ), "No warning-level log entry for a failed login attempt"

        Why it's skipped: `backend/logger.py` defines a configured
        structured logger (see docs/guides/LOGGING.md for the intended
        usage), but nothing in `backend/routers/auth.py` actually calls it
        on a failed login, a lockout, or any other authentication event.
        There's no log line for this test to detect - writing the test
        without wiring up the logging call it depends on would just be a
        test that always fails, which isn't the same as a placeholder.

        How you would implement it: add `logger.warning("failed login
        attempt", extra={"extra_fields": {"email": email}})` (careful not
        to log the attempted password) at the point in auth.py where a
        login is rejected for bad credentials, then use pytest's `caplog`
        fixture (for an in-process test) or query the log destination
        directly (for an end-to-end test against a running deployment) to
        assert the entry appeared.

        What you would actually do in production: this is exactly the kind
        of event a SIEM or log-based alerting rule watches for repeated
        occurrences from the same IP or against the same account, as an
        early signal of a credential-stuffing attempt - the test matters
        less than making sure the log line exists at all, since you can't
        alert on an event that was never recorded.
        """

    @pytest.mark.skip(
        reason="Same underlying gap as the failed-login test above: no "
        "code path in this app currently logs authorization failures."
    )
    def test_authorization_failures_are_logged(self, api_client):
        """
        What this test would do: Have one user attempt to edit or delete
        another user's post (the same scenario TestAuthorization already
        covers for the 403 response itself, in test_security.py), and
        additionally assert that the rejected attempt produced a log entry
        identifying who attempted it and what they attempted to access.

            with caplog.at_level(logging.WARNING, logger="testbook.posts"):
                api_client.put(f"{BASE_URL}/posts/1", json={...}, headers=mike_headers)
            assert any(
                "unauthorized" in r.message.lower() and "post" in r.message.lower()
                for r in caplog.records
            )

        Why it's skipped: like the login case, there's no logging call in
        the route handlers that reject these requests today - the 403
        itself is correct and already tested, but nothing records that it
        happened anywhere durable.

        How you would implement it: add a `logger.warning(...)` call at
        each point a request is rejected for an ownership/permission
        check, including the user ID making the attempt and the resource
        ID they tried to access, then assert on it the same way as the
        login test.

        What you would actually do in production: a single failed edit
        attempt is normal (a stale UI, a bookmarked URL) and not worth
        alerting on by itself; what's worth watching is the same user ID
        or IP racking up many of these across different resources in a
        short window, which is a monitoring/alerting concern layered on
        top of the logging, not something a single test can demonstrate.
        """
