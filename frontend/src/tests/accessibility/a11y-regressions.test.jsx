/**
 * Accessibility regression tests.
 *
 * Each describe block guards one defect from docs/a11y/AUDIT_LOG.md (the ID is in
 * the block name). They exist because the generic axe scans in
 * accessibility.test.jsx pass on all of these: axe accepts a placeholder as a
 * name, cannot see focus management, and only scans the state you render.
 *
 * What lives here vs. in the Playwright suite: anything that needs a real
 * browser (computed CSS, layout, tab order across a page, contrast) is tested in
 * tests/e2e/accessibility-behavior.spec.js. jsdom has no layout engine, so it
 * cannot check those.
 */

import { act, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { axe } from 'vitest-axe';
import { AuthContext } from '../../AuthContext';
import Alert from '../../components/Alert';
import ErrorBoundary from '../../components/ErrorBoundary';
import CreatePost from '../../components/CreatePost';
import LiveRegion, { announce } from '../../components/LiveRegion';
import Post from '../../components/Post';
import Feed from '../../pages/Feed';
import Login from '../../pages/Login';
import Register from '../../pages/Register';

vi.mock('../../api', () => ({
  feedAPI: {
    getAllFeed: vi.fn().mockResolvedValue({ data: [] }),
    getFollowingFeed: vi.fn().mockResolvedValue({ data: [] }),
  },
  postsAPI: {
    createPost: vi.fn(),
    updatePost: vi.fn(),
    deletePost: vi.fn(),
    addReaction: vi.fn(),
    removeReaction: vi.fn(),
    addComment: vi.fn(),
    createRepost: vi.fn(),
    deleteRepost: vi.fn(),
  },
}));

const futureFlags = { v7_startTransition: true, v7_relativeSplatPath: true };
const NO_CONTRAST = { rules: { 'color-contrast': { enabled: false } } }; // needs canvas; covered in e2e

const sarah = { id: 1, username: 'sarahjohnson', display_name: 'Sarah Johnson' };
const basePost = {
  id: 7,
  content: 'Hello Testbook!',
  author_id: 1,
  author_username: 'sarahjohnson',
  author_display_name: 'Sarah Johnson',
  author_profile_picture: '/static/uploads/avatars/sarah.jpg',
  created_at: '2026-01-15T10:00:00Z',
  image_url: null,
  video_url: null,
  is_repost: false,
  original_post_id: null,
  original_post: null,
  reactions_count: 0,
  comments_count: 0,
  reposts_count: 0,
  user_reaction: null,
  has_reposted: false,
};

const renderWith = (ui, auth = { user: sarah }) =>
  render(
    <BrowserRouter future={futureFlags}>
      <AuthContext.Provider value={auth}>{ui}</AuthContext.Provider>
    </BrowserRouter>
  );

const renderPost = (post = basePost, props = {}) =>
  renderWith(<Post post={post} onDelete={vi.fn()} onUpdate={vi.fn()} {...props} />);

describe('A11Y-001: form fields have a real accessible name, not just a placeholder', () => {
  it('Login fields are reachable by label', () => {
    renderWith(<Login />, { login: vi.fn() });
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
  });

  it('Register fields are reachable by label', () => {
    renderWith(<Register />, { register: vi.fn() });
    for (const name of ['Email', /^Username/, 'Display Name', 'Password', /^Bio/]) {
      expect(screen.getByLabelText(name)).toBeInTheDocument();
    }
  });

  it('the create-post textarea and the comment input have names', async () => {
    const user = userEvent.setup();
    renderWith(<CreatePost onPostCreated={vi.fn()} />);
    expect(screen.getByRole('textbox', { name: "What's on your mind?" })).toBeInTheDocument();

    renderPost();
    await user.click(screen.getByRole('button', { name: 'Comment' }));
    expect(screen.getByRole('textbox', { name: 'Write a comment' })).toBeInTheDocument();
  });
});

describe('A11Y-002: the post edit textarea has an accessible name', () => {
  it('names the textarea once edit mode is open, and axe is clean in that state', async () => {
    const user = userEvent.setup();
    const { container } = renderPost();

    await user.click(screen.getByRole('button', { name: 'Post options' }));
    await user.click(screen.getByRole('button', { name: /edit/i }));

    expect(screen.getByRole('textbox', { name: 'Edit post content' })).toBeInTheDocument();
    expect((await axe(container, NO_CONTRAST)).violations).toEqual([]);
  });
});

describe('A11Y-003: auth fields declare autocomplete tokens', () => {
  it('Login uses username / current-password', () => {
    renderWith(<Login />, { login: vi.fn() });
    expect(screen.getByLabelText('Email')).toHaveAttribute('autocomplete', 'username');
    expect(screen.getByLabelText('Password')).toHaveAttribute('autocomplete', 'current-password');
  });

  it('Register uses email / username / name / new-password', () => {
    renderWith(<Register />, { register: vi.fn() });
    expect(screen.getByLabelText('Email')).toHaveAttribute('autocomplete', 'email');
    expect(screen.getByLabelText(/^Username/)).toHaveAttribute('autocomplete', 'username');
    expect(screen.getByLabelText('Display Name')).toHaveAttribute('autocomplete', 'name');
    expect(screen.getByLabelText('Password')).toHaveAttribute('autocomplete', 'new-password');
  });

  it('password fields do not block paste (WCAG 3.3.8)', () => {
    renderWith(<Login />, { login: vi.fn() });
    expect(screen.getByLabelText('Password')).not.toHaveAttribute('onpaste');
  });
});

describe('A11Y-004: errors are announced and focus is not lost', () => {
  it('Alert exposes errors as role=alert and confirmations as role=status', () => {
    render(
      <>
        <Alert data-testid="e">Bad</Alert>
        <Alert type="success" data-testid="s">
          Saved
        </Alert>
      </>
    );
    expect(screen.getByTestId('e')).toHaveAttribute('role', 'alert');
    expect(screen.getByTestId('s')).toHaveAttribute('role', 'status');
  });

  it('a failed login shows a role=alert message and moves focus to it', async () => {
    const user = userEvent.setup();
    const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    const login = vi.fn().mockRejectedValue({ response: { data: { detail: 'Incorrect email' } } });
    renderWith(<Login />, { login });

    await user.type(screen.getByLabelText('Email'), 'a@b.com');
    await user.type(screen.getByLabelText('Password'), 'nope');
    await user.click(screen.getByRole('button', { name: 'Log In' }));

    const alert = await screen.findByRole('alert');
    expect(alert).toHaveTextContent('Incorrect email');
    // The submit button was disabled mid-request; without this, focus is on <body>.
    await waitFor(() => expect(alert).toHaveFocus());
    errorSpy.mockRestore();
  });
});

describe('A11Y-005: no interactive element is nested inside another', () => {
  it('the "View" control is a single link, not a button inside a link', () => {
    const { container } = renderPost();
    expect(container.querySelectorAll('a button, button a')).toHaveLength(0);
    const view = screen.getByRole('link', { name: 'View post by Sarah Johnson' });
    expect(view).toHaveAttribute('href', '/post/7');
  });

  it('Login and Register cross-links are single links too', () => {
    const { container: login } = renderWith(<Login />, { login: vi.fn() });
    expect(login.querySelectorAll('a button, button a')).toHaveLength(0);
    const { container: register } = renderWith(<Register />, { register: vi.fn() });
    expect(register.querySelectorAll('a button, button a')).toHaveLength(0);
  });
});

describe('A11Y-006: icon-only and disclosure controls have names and state', () => {
  it('the menu button is named and reports expanded/collapsed', async () => {
    const user = userEvent.setup();
    renderPost();
    const menu = screen.getByRole('button', { name: 'Post options' });

    expect(menu).toHaveAttribute('aria-expanded', 'false');
    await user.click(menu);
    expect(menu).toHaveAttribute('aria-expanded', 'true');
    expect(menu).toHaveAttribute('aria-controls', screen.getByTestId('post-7-dropdown').id);
  });

  it('the react button reports expanded and names the current reaction', async () => {
    const user = userEvent.setup();
    const { rerender } = renderPost();
    const react = screen.getByRole('button', { name: 'React' });

    expect(react).toHaveAttribute('aria-expanded', 'false');
    react.focus();
    await user.keyboard('{Enter}');
    expect(react).toHaveAttribute('aria-expanded', 'true');

    rerender(
      <BrowserRouter future={futureFlags}>
        <AuthContext.Provider value={{ user: sarah }}>
          <Post
            post={{ ...basePost, user_reaction: 'love' }}
            onDelete={vi.fn()}
            onUpdate={vi.fn()}
          />
        </AuthContext.Provider>
      </BrowserRouter>
    );
    expect(
      screen.getByRole('button', { name: 'Your reaction: love. Change reaction' })
    ).toBeInTheDocument();
  });

  it('each reaction option has a text name and exposes its pressed state', async () => {
    const user = userEvent.setup();
    renderPost({ ...basePost, user_reaction: 'wow' });
    screen.getByRole('button', { name: /Your reaction: wow/ }).focus();
    await user.keyboard('{Enter}');
    for (const name of ['Like', 'Love', 'Haha', 'Wow', 'Sad', 'Angry']) {
      expect(screen.getByRole('button', { name })).toHaveAttribute(
        'aria-pressed',
        String(name === 'Wow')
      );
    }
  });

  it('the post is a named article so repeated button names have context', () => {
    renderPost();
    expect(screen.getByRole('article', { name: 'Post by Sarah Johnson' })).toBeInTheDocument();
  });
});

describe('A11Y-007: focus goes somewhere sensible when controls open and close', () => {
  it('Edit moves focus into the textarea; Cancel returns it to the menu button', async () => {
    const user = userEvent.setup();
    renderPost();

    await user.click(screen.getByRole('button', { name: 'Post options' }));
    await user.click(screen.getByRole('button', { name: /edit/i }));
    expect(screen.getByRole('textbox', { name: 'Edit post content' })).toHaveFocus();

    await user.click(screen.getByRole('button', { name: 'Cancel' }));
    expect(screen.getByRole('button', { name: 'Post options' })).toHaveFocus();
  });

  it('Escape closes the menu and returns focus to its button', async () => {
    const user = userEvent.setup();
    renderPost();
    const menu = screen.getByRole('button', { name: 'Post options' });

    await user.click(menu);
    expect(screen.getByTestId('post-7-dropdown')).toBeInTheDocument();
    await user.keyboard('{Escape}');

    expect(screen.queryByTestId('post-7-dropdown')).not.toBeInTheDocument();
    expect(menu).toHaveFocus();
  });

  it('Escape closes the reaction picker and returns focus to the react button', async () => {
    const user = userEvent.setup();
    renderPost();
    const react = screen.getByRole('button', { name: 'React' });

    react.focus();
    await user.keyboard('{Enter}');
    expect(react).toHaveAttribute('aria-expanded', 'true');
    await user.keyboard('{Escape}');

    expect(react).toHaveAttribute('aria-expanded', 'false');
    expect(react).toHaveFocus();
  });

  it('opening the comment box focuses its input; closing it returns focus to the button', async () => {
    const user = userEvent.setup();
    renderPost();
    const toggle = screen.getByRole('button', { name: 'Comment' });

    await user.click(toggle);
    expect(screen.getByRole('textbox', { name: 'Write a comment' })).toHaveFocus();

    await user.click(toggle);
    expect(toggle).toHaveFocus();
  });
});

describe('A11Y-012: a closed reaction picker is not in the tab order', () => {
  it('hides the six reaction buttons until the picker is opened', async () => {
    const user = userEvent.setup();
    renderPost();

    // visibility:hidden (from Post.css, applied by jsdom) removes them from the
    // accessibility tree and the tab order. opacity:0 alone would not.
    expect(screen.queryByRole('button', { name: 'Like' })).not.toBeInTheDocument();

    screen.getByRole('button', { name: 'React' }).focus();
    await user.keyboard('{Enter}');
    expect(screen.getByRole('button', { name: 'Like' })).toBeInTheDocument();
  });
});

describe('A11Y-014: hover and click do not fight over the reaction picker', () => {
  it('a mouse click leaves the picker open and aria-expanded true', async () => {
    const user = userEvent.setup();
    renderPost();
    const react = screen.getByRole('button', { name: 'React' });

    // user.click() hovers first, then clicks - exactly what a real mouse does.
    // Before the fix, hover opened the picker and the click toggled it shut again.
    await user.click(react);

    expect(react).toHaveAttribute('aria-expanded', 'true');
    expect(screen.getByRole('button', { name: 'Like' })).toBeInTheDocument();
  });

  it('moving the pointer away does not close a picker opened by keyboard', async () => {
    const user = userEvent.setup();
    renderPost();
    const react = screen.getByRole('button', { name: 'React' });

    react.focus();
    await user.keyboard('{Enter}');
    await user.hover(screen.getByRole('button', { name: 'Like' }));
    await user.unhover(screen.getByRole('button', { name: 'Like' }));

    expect(react).toHaveAttribute('aria-expanded', 'true');
  });

  it('clicking elsewhere closes the picker', async () => {
    const user = userEvent.setup();
    renderPost();
    const react = screen.getByRole('button', { name: 'React' });

    await user.click(react);
    await user.click(document.body);

    expect(react).toHaveAttribute('aria-expanded', 'false');
  });
});

describe('A11Y-015: the active Feed tab is exposed, not just coloured', () => {
  it('marks exactly one tab as pressed and follows the selection', async () => {
    const user = userEvent.setup();
    renderWith(<Feed />);

    const all = screen.getByRole('button', { name: 'See All' });
    const following = screen.getByRole('button', { name: 'Following' });
    expect(all).toHaveAttribute('aria-pressed', 'true');
    expect(following).toHaveAttribute('aria-pressed', 'false');

    await user.click(following);
    expect(all).toHaveAttribute('aria-pressed', 'false');
    expect(following).toHaveAttribute('aria-pressed', 'true');
  });
});

describe('A11Y-017: ids referenced by aria-controls are unique in the document', () => {
  it('a post and a repost of it, on the same page, do not duplicate any id', () => {
    // The feed shows post 3 AND a repost of post 3 (which embeds post 3 again).
    const original = { ...basePost, id: 3, content: 'The original' };
    const repost = {
      ...basePost,
      id: 9,
      is_repost: true,
      original_post_id: 3,
      original_post: original,
    };
    const { container } = renderWith(
      <>
        <Post post={original} onDelete={vi.fn()} onUpdate={vi.fn()} />
        <Post post={repost} onDelete={vi.fn()} onUpdate={vi.fn()} />
      </>
    );

    const ids = [...container.querySelectorAll('[id]')].map((el) => el.id);
    expect(ids.length).toBeGreaterThan(0);
    expect(new Set(ids).size).toBe(ids.length);

    // ...and every aria-controls that is expanded points at exactly one element.
    // (A collapsed menu has nothing to point at yet, which ARIA allows.)
    for (const el of container.querySelectorAll('[aria-controls][aria-expanded="true"]')) {
      expect(container.querySelectorAll(`[id="${el.getAttribute('aria-controls')}"]`)).toHaveLength(
        1
      );
    }
  });
});

describe('A11Y-018: Escape dismisses a hover-revealed picker (WCAG 1.4.13)', () => {
  it('marks the picker dismissed on Escape while hovering, and resets on mouse-leave', async () => {
    const user = userEvent.setup();
    const { container } = renderPost();
    const wrapper = container.querySelector('.reactions-container');

    // jsdom cannot evaluate :hover, so assert the state the CSS keys off.
    await user.hover(screen.getByRole('button', { name: 'React' }));
    expect(wrapper).not.toHaveClass('hover-dismissed');

    await user.keyboard('{Escape}');
    expect(wrapper).toHaveClass('hover-dismissed');

    await user.unhover(screen.getByRole('button', { name: 'React' }));
    expect(wrapper).not.toHaveClass('hover-dismissed');
  });

  it('does not touch aria-expanded, which only click and keyboard control', async () => {
    const user = userEvent.setup();
    renderPost();
    const react = screen.getByRole('button', { name: 'React' });

    await user.hover(react);
    await user.keyboard('{Escape}');

    expect(react).toHaveAttribute('aria-expanded', 'false');
  });
});

describe('A11Y-019: an unexpected API error shape must not blank the page', () => {
  // The real body of a 422 from POST /api/auth/register with the email "a@b".
  const validationError = {
    response: {
      data: {
        detail: [
          {
            type: 'value_error',
            loc: ['body', 'email'],
            msg: 'value is not a valid email address: The part after the @-sign is not valid.',
            input: 'a@b',
          },
        ],
      },
    },
  };

  it('Register shows a readable alert for a list-shaped (422) error instead of crashing', async () => {
    const user = userEvent.setup();
    const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    renderWith(<Register />, { register: vi.fn().mockRejectedValue(validationError) });

    await user.type(screen.getByLabelText('Email'), 'a@b');
    await user.type(screen.getByLabelText(/^Username/), 'zed');
    await user.type(screen.getByLabelText('Display Name'), 'Zed');
    await user.type(screen.getByLabelText('Password'), 'Password1!');
    await user.click(screen.getByRole('button', { name: 'Sign Up' }));

    const alert = await screen.findByRole('alert');
    expect(alert).toHaveTextContent('Enter a valid email address');
    // The page is still there: the form was not unmounted by a render crash.
    expect(screen.getByRole('heading', { name: 'Create Account' })).toBeInTheDocument();
    errorSpy.mockRestore();
  });

  it('Login does the same', async () => {
    const user = userEvent.setup();
    const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    renderWith(<Login />, { login: vi.fn().mockRejectedValue(validationError) });

    await user.type(screen.getByLabelText('Email'), 'a@b');
    await user.type(screen.getByLabelText('Password'), 'x');
    await user.click(screen.getByRole('button', { name: 'Log In' }));

    expect(await screen.findByRole('alert')).toHaveTextContent('Enter a valid email address');
    errorSpy.mockRestore();
  });

  it('ErrorBoundary replaces a crashed tree with a readable, focused explanation', () => {
    const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    const Bomb = () => {
      throw new Error('boom');
    };
    render(
      <ErrorBoundary>
        <Bomb />
      </ErrorBoundary>
    );

    // Not a blank page: there is a heading, and focus is on it so assistive technology reads it.
    const heading = screen.getByRole('heading', { name: 'Something went wrong' });
    expect(heading).toHaveFocus();
    expect(screen.getByRole('button', { name: 'Reload the page' })).toBeInTheDocument();
    expect(document.title).toBe('Something went wrong - Testbook');
    errorSpy.mockRestore();
  });

  it('ErrorBoundary renders its children when nothing is wrong', () => {
    render(
      <ErrorBoundary>
        <p>All fine</p>
      </ErrorBoundary>
    );
    expect(screen.getByText('All fine')).toBeInTheDocument();
  });
});

describe('A11Y-013: changes with no visible message are announced', () => {
  it('announce() writes to the polite live region', async () => {
    render(<LiveRegion />);
    const region = screen.getByTestId('live-region');
    expect(region).toHaveAttribute('aria-live', 'polite');

    act(() => announce('Reacted with like'));
    await waitFor(() => expect(region).toHaveTextContent('Reacted with like'));
  });

  it('announcing the same text twice still re-announces it', async () => {
    render(<LiveRegion />);
    const region = screen.getByTestId('live-region');

    act(() => announce('Reposted'));
    await waitFor(() => expect(region).toHaveTextContent('Reposted'));
    act(() => announce('Reposted'));
    // Cleared first, then re-set - that gap is what makes a screen reader speak it again.
    await waitFor(() => expect(region).toHaveTextContent(''));
    await waitFor(() => expect(region).toHaveTextContent('Reposted'));
  });
});

describe('A11Y-009: each page sets its own document title', () => {
  it('Login and Register have distinct titles', () => {
    const { unmount } = renderWith(<Login />, { login: vi.fn() });
    expect(document.title).toBe('Log In - Testbook');
    unmount();

    renderWith(<Register />, { register: vi.fn() });
    expect(document.title).toBe('Sign Up - Testbook');
  });
});

describe('axe in states the default-page scans never reach', () => {
  beforeEach(() => vi.clearAllMocks());

  it('comment box open', async () => {
    const user = userEvent.setup();
    const { container } = renderPost();
    await user.click(screen.getByRole('button', { name: 'Comment' }));
    expect((await axe(container, NO_CONTRAST)).violations).toEqual([]);
  });

  it('menu open', async () => {
    const user = userEvent.setup();
    const { container } = renderPost();
    await user.click(screen.getByRole('button', { name: 'Post options' }));
    expect((await axe(container, NO_CONTRAST)).violations).toEqual([]);
  });

  it('reaction picker open', async () => {
    const user = userEvent.setup();
    const { container } = renderPost();
    screen.getByRole('button', { name: 'React' }).focus();
    await user.keyboard('{Enter}');
    expect((await axe(container, NO_CONTRAST)).violations).toEqual([]);
  });
});
