"""
Accessibility tests - Python/Playwright (WCAG 2.2 AA).

The Python twin of tests/e2e/accessibility-axe.spec.js and accessibility-behavior.spec.js. The
same checks, in the same order, written with Python's idioms, so you can compare the two tracks
line by line (see docs/a11y/JS_VS_PYTHON_ACCESSIBILITY_TESTING.md).

Two kinds of test, because axe sees only a snapshot:

  1. axe scans: every route, interaction states, dark theme, and a 320 px phone width.
  2. Behaviour tests: focus, tab order, announcements, reflow, sticky-header coverage - the things
     a snapshot cannot see.

Each behaviour test names the audit finding it guards (docs/a11y/AUDIT_LOG.md).

Run with:  pytest -m a11y -v
"""

import re

import pytest
from playwright.sync_api import Page, expect

from a11y import expect_no_a11y_violations, press_tab
from pages.auth_page import AuthPage

pytestmark = pytest.mark.a11y

PUBLIC_ROUTES = [("Login", "/login"), ("Register", "/register")]
AUTHENTICATED_ROUTES = [
    ("Feed", "/"),
    ("Profile", "/profile/sarahjohnson"),
    ("Followers", "/profile/sarahjohnson/followers"),
    ("Following", "/profile/sarahjohnson/following"),
    ("Settings", "/settings"),
]


def login_as_sarah(page: Page, base_url: str, test_users: dict) -> None:
    auth = AuthPage(page)
    auth.goto_login()
    auth.login(test_users["sarah"]["email"], test_users["sarah"]["password"])
    auth.expect_logged_in()
    try:
        page.get_by_test_id("post-1").wait_for(timeout=5000)
    except Exception:  # the seed post may not be first; the navbar being visible is enough
        pass


def open_first_post_detail(page: Page, base_url: str) -> None:
    href = page.locator('a[href^="/post/"]').first.get_attribute("href")
    page.goto(f"{base_url}{href}")
    page.wait_for_load_state("networkidle")


def settle(page: Page) -> None:
    try:
        page.wait_for_load_state("networkidle", timeout=5000)
    except Exception:
        pass


def focused(page: Page) -> str:
    """A short, stable description of the focused element, for tab-order assertions."""
    return page.evaluate(
        """() => {
            const el = document.activeElement;
            return el.getAttribute('data-testid') || el.getAttribute('id') ||
                   el.getAttribute('aria-label') || el.tagName.toLowerCase();
        }"""
    )


def own_post_id(page: Page) -> str:
    return page.locator('[data-is-own-post="true"]').first.get_attribute("data-post-id")


# ---------------------------------------------------------------------------------------------
# 1. axe scans
# ---------------------------------------------------------------------------------------------


class TestAxeRoutes:
    @pytest.mark.parametrize(("name", "path"), PUBLIC_ROUTES)
    def test_public_page(self, page, base_url, fresh_database, name, path):
        page.goto(f"{base_url}{path}")
        settle(page)
        expect_no_a11y_violations(page, name)

    @pytest.mark.parametrize(("name", "path"), AUTHENTICATED_ROUTES)
    def test_authenticated_page(self, page, base_url, test_users, fresh_database, name, path):
        login_as_sarah(page, base_url, test_users)
        page.goto(f"{base_url}{path}")
        settle(page)
        expect_no_a11y_violations(page, name)

    def test_post_detail_page(self, page, base_url, test_users, fresh_database):
        login_as_sarah(page, base_url, test_users)
        open_first_post_detail(page, base_url)
        expect_no_a11y_violations(page, "Post detail")


class TestAxeInteractionStates:
    """Several real defects only existed once something was open or showing, so a scan of the
    default page missed them."""

    def test_login_with_an_error_showing(self, page, base_url, fresh_database):
        page.goto(f"{base_url}/login")
        page.get_by_label("Email").fill("nobody@example.com")
        page.get_by_label("Password").fill("wrong-password")
        page.get_by_role("button", name="Log In").click()
        page.get_by_role("alert").wait_for()
        expect_no_a11y_violations(page, "Login error")  # catches the error failing contrast

    def test_register_with_an_error_showing(self, page, base_url, test_users, fresh_database):
        page.goto(f"{base_url}/register")
        page.get_by_label("Email").fill(test_users["sarah"]["email"])  # already taken
        page.get_by_label(re.compile("^Username")).fill("someone")
        page.get_by_label("Display Name").fill("Someone")
        page.get_by_label("Password").fill("Password123!")
        page.get_by_role("button", name="Sign Up").click()
        page.get_by_role("alert").wait_for()
        expect_no_a11y_violations(page, "Register error")

    def test_feed_with_a_post_menu_open(self, page, base_url, test_users, fresh_database):
        login_as_sarah(page, base_url, test_users)
        page.get_by_role("button", name="Post options").first.click()
        expect_no_a11y_violations(page, "Post menu open")

    def test_feed_with_a_post_in_edit_mode(self, page, base_url, test_users, fresh_database):
        login_as_sarah(page, base_url, test_users)
        page.get_by_role("button", name="Post options").first.click()
        page.get_by_role("button", name=re.compile("Edit")).click()
        page.get_by_role("textbox", name="Edit post content").wait_for()
        expect_no_a11y_violations(page, "Post edit mode")  # catches the unlabeled edit textarea

    def test_feed_with_a_comment_box_open(self, page, base_url, test_users, fresh_database):
        login_as_sarah(page, base_url, test_users)
        page.get_by_role("button", name="Comment").first.click()
        page.get_by_role("textbox", name="Write a comment").wait_for()
        expect_no_a11y_violations(page, "Comment box open")

    def test_feed_with_a_reaction_picker_open(self, page, base_url, test_users, fresh_database):
        login_as_sarah(page, base_url, test_users)
        page.get_by_role("button", name="React", exact=True).first.click()
        page.get_by_role("button", name="Like", exact=True).first.wait_for()
        expect_no_a11y_violations(page, "Reaction picker open")


class TestAxePhoneWidth:
    @pytest.fixture(autouse=True)
    def phone_viewport(self, page):
        page.set_viewport_size({"width": 320, "height": 700})

    @pytest.mark.parametrize(("name", "path"), PUBLIC_ROUTES)
    def test_public_page(self, page, base_url, fresh_database, name, path):
        page.goto(f"{base_url}{path}")
        settle(page)
        expect_no_a11y_violations(page, f"{name} @320")

    @pytest.mark.parametrize(("name", "path"), AUTHENTICATED_ROUTES)
    def test_authenticated_page(self, page, base_url, test_users, fresh_database, name, path):
        login_as_sarah(page, base_url, test_users)
        page.goto(f"{base_url}{path}")
        settle(page)
        expect_no_a11y_violations(page, f"{name} @320")


class TestAxeDarkTheme:
    """The theme is a per-user setting, so go through the real Settings flow. The original suite
    never scanned dark mode, and it hid real contrast failures (white on the dark accent: 3.45:1)."""

    @pytest.fixture(autouse=True)
    def dark_theme(self, page, base_url, test_users, fresh_database):
        login_as_sarah(page, base_url, test_users)
        page.goto(f"{base_url}/settings")
        page.get_by_label("Theme").select_option("dark")
        page.get_by_role("button", name=re.compile("save", re.IGNORECASE)).click()
        page.get_by_role("status").wait_for()
        expect(page.locator("html")).to_have_attribute("data-theme", "dark")

    @pytest.mark.parametrize(("name", "path"), AUTHENTICATED_ROUTES)
    def test_authenticated_page(self, page, base_url, name, path):
        page.goto(f"{base_url}{path}")
        settle(page)
        expect(page.locator("html")).to_have_attribute("data-theme", "dark")
        expect_no_a11y_violations(page, f"{name} (dark)")

    def test_post_detail_page(self, page, base_url):
        page.goto(f"{base_url}/")
        open_first_post_detail(page, base_url)
        expect(page.locator("html")).to_have_attribute("data-theme", "dark")
        expect_no_a11y_violations(page, "Post detail (dark)")

    def test_feed_with_the_reaction_picker_open(self, page, base_url):
        page.goto(f"{base_url}/")
        page.get_by_role("button", name="React", exact=True).first.click()
        page.get_by_role("button", name="Like", exact=True).first.wait_for()
        expect_no_a11y_violations(page, "Reaction picker (dark)")


# ---------------------------------------------------------------------------------------------
# 2. Behaviour tests (what axe cannot see)
# ---------------------------------------------------------------------------------------------


class TestBehaviour:
    def test_login_tab_order_is_email_password_submit_create_account(self, page, base_url, fresh_database):
        """2.4.3"""
        page.goto(f"{base_url}/login")
        # Keys fire instantly: wait for the form to exist or the first Tab lands on nothing.
        expect(page.get_by_label("Email")).to_be_visible()
        order = []
        for _ in range(4):
            press_tab(page)
            order.append(focused(page))
        assert order == [
            "login-email-input",
            "login-password-input",
            "login-submit-button",
            "create-account-button",
        ]

    def test_login_works_by_keyboard_alone(self, page, base_url, test_users, fresh_database):
        """2.1.1"""
        page.goto(f"{base_url}/login")
        expect(page.get_by_label("Email")).to_be_visible()
        press_tab(page)
        page.keyboard.type(test_users["sarah"]["email"])
        press_tab(page)
        page.keyboard.type(test_users["sarah"]["password"])
        page.keyboard.press("Enter")
        expect(page.get_by_test_id("navbar")).to_be_visible()

    def test_password_fields_accept_paste(self, page, base_url, fresh_database):
        """A11Y-003 / 3.3.8"""
        page.goto(f"{base_url}/login")
        blocked = page.get_by_label("Password").evaluate(
            """el => {
                const event = new Event('paste', { bubbles: true, cancelable: true });
                el.dispatchEvent(event);
                return event.defaultPrevented;
            }"""
        )
        assert blocked is False

    def test_a_failed_login_is_announced_and_takes_focus(self, page, base_url, fresh_database):
        """A11Y-004 / 4.1.3, 2.4.3"""
        page.goto(f"{base_url}/login")
        page.get_by_label("Email").fill("nobody@example.com")
        page.get_by_label("Password").fill("wrong-password")
        page.keyboard.press("Enter")

        alert = page.get_by_role("alert")
        expect(alert).to_be_visible()
        # Focus must not fall back to <body> when the submit button re-enables.
        expect(alert).to_be_focused()

    def test_every_route_has_its_own_title(self, page, base_url, test_users, fresh_database):
        """A11Y-009 / 2.4.2"""
        page.goto(f"{base_url}/login")
        expect(page).to_have_title("Log In - Testbook")
        page.goto(f"{base_url}/register")
        expect(page).to_have_title("Sign Up - Testbook")

        login_as_sarah(page, base_url, test_users)
        expect(page).to_have_title("Home - Testbook")
        page.goto(f"{base_url}/settings")
        expect(page).to_have_title("Settings - Testbook")
        page.goto(f"{base_url}/profile/sarahjohnson")
        expect(page).to_have_title("Sarah Johnson (@sarahjohnson) - Testbook")
        page.goto(f"{base_url}/profile/sarahjohnson/followers")
        expect(page).to_have_title("Followers of @sarahjohnson - Testbook")
        page.goto(f"{base_url}/profile/sarahjohnson/following")
        expect(page).to_have_title("People @sarahjohnson follows - Testbook")
        page.goto(f"{base_url}/post/1")
        expect(page).to_have_title(re.compile(r"^Post by .+ - Testbook$"))

    def test_client_side_navigation_is_announced(self, page, base_url, test_users, fresh_database):
        """A11Y-013 / 4.1.3"""
        login_as_sarah(page, base_url, test_users)
        page.get_by_test_id("navbar-settings-link").click()
        expect(page.get_by_test_id("live-region")).to_have_text("Settings - Testbook")

    def test_a_skip_link_is_the_first_tab_stop_and_moves_focus_to_main(
        self, page, base_url, test_users, fresh_database
    ):
        """A11Y-010 / 2.4.1"""
        login_as_sarah(page, base_url, test_users)
        press_tab(page)
        skip = page.get_by_role("link", name="Skip to main content")
        expect(skip).to_be_focused()
        expect(skip).to_be_visible()  # not just focusable: visible once focused

        page.keyboard.press("Enter")
        expect(page.locator("main")).to_be_focused()

    def test_inputs_show_a_focus_indicator(self, page, base_url, fresh_database):
        """A11Y-011 / 2.4.7, 1.4.11"""
        page.goto(f"{base_url}/login")
        press_tab(page)  # keyboard focus, so :focus-visible applies
        style = page.get_by_label("Email").evaluate(
            """el => { const s = getComputedStyle(el);
                       return { style: s.outlineStyle, width: parseFloat(s.outlineWidth) }; }"""
        )
        assert style["style"] != "none"
        assert style["width"] >= 2

    def test_no_horizontal_scroll_at_320px(self, page, base_url, test_users, fresh_database):
        """A11Y-008 / 1.4.10"""
        page.set_viewport_size({"width": 320, "height": 700})
        login_as_sarah(page, base_url, test_users)
        for path in ["/", "/settings", "/profile/sarahjohnson", "/post/1"]:
            page.goto(f"{base_url}{path}")
            page.wait_for_load_state("networkidle")
            overflow = page.evaluate(
                "document.documentElement.scrollWidth - document.documentElement.clientWidth"
            )
            assert overflow <= 0, f"{path} overflows by {overflow}px"

    def test_closed_reaction_pickers_add_no_tab_stops(self, page, base_url, test_users, fresh_database):
        """A11Y-012 / 2.4.7"""
        login_as_sarah(page, base_url, test_users)
        page.mouse.click(5, 300)  # park focus at the top of the page
        stops = []
        for _ in range(40):
            press_tab(page)
            stops.append(focused(page))
        assert [s for s in stops if "-reaction-" in s] == []

    def test_the_reaction_picker_opens_and_closes_by_keyboard(
        self, page, base_url, test_users, fresh_database
    ):
        """A11Y-006 / 2.1.1"""
        login_as_sarah(page, base_url, test_users)
        # exact=True: "React" would otherwise also match "Your reaction: like. Change reaction"
        react = page.get_by_role("button", name="React", exact=True).first
        react.focus()
        page.keyboard.press("Enter")
        expect(react).to_have_attribute("aria-expanded", "true")
        # Wait until the picker is visible (it fades in) before tabbing: Tab skips hidden controls.
        like = page.get_by_role("button", name="Like", exact=True).first
        expect(like).to_be_visible()

        press_tab(page)
        expect(like).to_be_focused()

        page.keyboard.press("Escape")
        expect(react).to_have_attribute("aria-expanded", "false")
        expect(react).to_be_focused()

    def test_a_real_mouse_click_opens_the_picker_and_aria_expanded_agrees(
        self, page, base_url, test_users, fresh_database
    ):
        """A11Y-014"""
        login_as_sarah(page, base_url, test_users)
        react = page.get_by_role("button", name="React", exact=True).first
        react.click()  # Playwright hovers, then clicks, like a real pointer
        expect(react).to_have_attribute("aria-expanded", "true")
        expect(page.get_by_role("button", name="Like", exact=True).first).to_be_visible()

        # Moving the pointer away must not close it; clicking elsewhere does.
        page.mouse.move(0, 0)
        expect(react).to_have_attribute("aria-expanded", "true")
        page.mouse.click(5, 300)
        expect(react).to_have_attribute("aria-expanded", "false")

    def test_no_duplicate_ids_on_the_feed(self, page, base_url, test_users, fresh_database):
        """A11Y-017 / 4.1.2 (aria-controls targets)"""
        login_as_sarah(page, base_url, test_users)
        # The seed data has reposts, which embed the original post: a second copy of a post
        # already on the page. Any id derived from the post id would collide.
        expect(page.locator('[data-is-repost="true"]').first).to_be_visible()
        duplicates = page.evaluate(
            """() => {
                const seen = new Map();
                for (const el of document.querySelectorAll('[id]')) {
                    seen.set(el.id, (seen.get(el.id) || 0) + 1);
                }
                return [...seen].filter(([, count]) => count > 1).map(([id]) => id);
            }"""
        )
        assert duplicates == []

    def test_the_active_feed_tab_is_exposed_to_assistive_technology(
        self, page, base_url, test_users, fresh_database
    ):
        """A11Y-015"""
        login_as_sarah(page, base_url, test_users)
        all_tab = page.get_by_role("button", name="See All")
        following = page.get_by_role("button", name="Following")
        expect(all_tab).to_have_attribute("aria-pressed", "true")
        following.click()
        expect(following).to_have_attribute("aria-pressed", "true")
        expect(all_tab).to_have_attribute("aria-pressed", "false")

    def test_escape_dismisses_a_hover_revealed_picker_without_moving_the_pointer(
        self, page, base_url, test_users, fresh_database
    ):
        """A11Y-018 / 1.4.13"""
        login_as_sarah(page, base_url, test_users)
        react = page.get_by_role("button", name="React", exact=True).first
        like = page.get_by_role("button", name="Like", exact=True).first

        react.hover()  # hover only: no click, no focus
        expect(like).to_be_visible()  # revealed by hover (CSS :hover)

        # Hoverable: the pointer can travel onto the picker without it vanishing.
        like.hover()
        expect(like).to_be_visible()

        # Dismissible: Escape hides it while the pointer stays exactly where it is.
        page.keyboard.press("Escape")
        expect(like).to_be_hidden()

        # Moving away and back brings it back.
        page.mouse.move(0, 0)
        react.hover()
        expect(like).to_be_visible()

    def test_a_validation_error_from_the_api_shows_a_readable_alert_not_a_blank_page(
        self, page, base_url, fresh_database
    ):
        """A11Y-019 / 3.3.1

        "a@b" passes the browser's own email check but the API rejects it with a 422 whose
        `detail` is a LIST of objects. Rendering that list used to crash React and blank the page.
        """
        page_errors = []
        page.on("pageerror", lambda error: page_errors.append(error.message))

        page.goto(f"{base_url}/register")
        page.get_by_label("Email").fill("a@b")
        page.get_by_label(re.compile("^Username")).fill("zed")
        page.get_by_label("Display Name").fill("Zed")
        page.get_by_label("Password").fill("Password1!")
        page.get_by_role("button", name="Sign Up").click()

        alert = page.get_by_role("alert")
        expect(alert).to_be_visible()
        expect(alert).to_contain_text("valid email address")
        # The page is still there: a crash would have removed the whole form.
        expect(page.get_by_role("heading", name="Create Account")).to_be_visible()
        assert page_errors == []

    def test_the_sticky_navbar_never_fully_covers_the_focused_element(
        self, page, base_url, test_users, fresh_database
    ):
        """2.4.11"""
        login_as_sarah(page, base_url, test_users)
        page.mouse.click(5, 300)
        nav_bottom = page.get_by_test_id("navbar").evaluate("el => el.getBoundingClientRect().bottom")

        for _ in range(80):
            press_tab(page)
            info = page.evaluate(
                """() => {
                    const el = document.activeElement;
                    return {
                        id: el.getAttribute('data-testid') || el.tagName,
                        bottom: el.getBoundingClientRect().bottom,
                        insideNavbar: !!el.closest('[data-testid="navbar"]'),
                    };
                }"""
            )
            # Entirely above the navbar's bottom edge means entirely hidden behind it (or scrolled
            # off); the navbar's own links sit inside it and are exempt.
            if not info["insideNavbar"]:
                assert info["bottom"] > nav_bottom, f"{info['id']} is hidden behind the navbar"

    def test_reacting_reposting_and_commenting_are_announced(self, page, base_url, test_users, fresh_database):
        """A11Y-013 / 4.1.3"""
        login_as_sarah(page, base_url, test_users)
        live = page.get_by_test_id("live-region")
        # A plain post, not a repost: a repost embeds its original, which repeats the original's
        # data-testids on the same page.
        post = page.locator('[data-post-id][data-is-repost="false"]').first
        post_id = post.get_attribute("data-post-id")

        # Scoped to this one post: ids repeat when a repost embeds its original.
        post.get_by_test_id(f"post-{post_id}-react-button").click()
        post.get_by_test_id(f"post-{post_id}-reaction-like").click()
        expect(live).to_have_text(re.compile("Reacted with like|Reaction removed"))

        post.get_by_test_id(f"post-{post_id}-comment-button").click()
        expect(post.get_by_test_id(f"post-{post_id}-comment-input")).to_be_focused()
        page.keyboard.type("Nice post")
        page.keyboard.press("Enter")
        expect(live).to_have_text("Comment posted")
        expect(post.get_by_test_id(f"post-{post_id}-comment-button")).to_be_focused()

    def test_interactive_controls_on_the_feed_are_at_least_24px(self, page, base_url, test_users, fresh_database):
        """2.5.8"""
        login_as_sarah(page, base_url, test_users)
        too_small = page.evaluate(
            """() => [...document.querySelectorAll('button, a[href], input, textarea, select')]
                .map(el => ({ el, r: el.getBoundingClientRect() }))
                .filter(({ r }) => r.width > 0 && r.height > 0 && (r.width < 24 || r.height < 24))
                .map(({ el, r }) => `${el.tagName} ${el.getAttribute('data-testid') || ''} ${Math.round(r.width)}x${Math.round(r.height)}`)"""
        )
        assert too_small == []


class TestFocusManagementInThePostCard:
    """2.4.3"""

    def test_edit_focuses_the_textarea_and_cancel_returns_to_the_menu_button(
        self, page, base_url, test_users, fresh_database
    ):
        """A11Y-007"""
        login_as_sarah(page, base_url, test_users)
        post_id = own_post_id(page)
        menu = page.get_by_test_id(f"post-{post_id}-menu-button")

        menu.click()
        expect(menu).to_have_attribute("aria-expanded", "true")
        page.get_by_test_id(f"post-{post_id}-edit-button").click()
        expect(page.get_by_test_id(f"post-{post_id}-edit-textarea")).to_be_focused()

        page.get_by_test_id(f"post-{post_id}-cancel-button").click()
        expect(menu).to_be_focused()

    def test_escape_closes_the_post_menu_and_returns_focus_to_its_button(
        self, page, base_url, test_users, fresh_database
    ):
        """A11Y-007"""
        login_as_sarah(page, base_url, test_users)
        post_id = own_post_id(page)
        menu = page.get_by_test_id(f"post-{post_id}-menu-button")

        menu.click()
        page.keyboard.press("Escape")
        expect(page.get_by_test_id(f"post-{post_id}-dropdown")).to_be_hidden()
        expect(menu).to_be_focused()

    def test_deleting_a_post_parks_focus_on_main_and_announces_it(
        self, page, base_url, test_users, fresh_database
    ):
        """A11Y-007 (the shared conftest page fixture already accepts the confirm() dialog)"""
        login_as_sarah(page, base_url, test_users)
        post_id = own_post_id(page)

        page.get_by_test_id(f"post-{post_id}-menu-button").click()
        page.get_by_test_id(f"post-{post_id}-delete-button").click()

        expect(page.get_by_test_id(f"post-{post_id}")).to_have_count(0)
        expect(page.locator("main")).to_be_focused()
        expect(page.get_by_test_id("live-region")).to_have_text("Post deleted")
