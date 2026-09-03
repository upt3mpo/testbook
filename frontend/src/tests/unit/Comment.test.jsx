/**
 * Unit tests for the Comment component.
 *
 * Comment is a small presentational component with no state or API
 * calls of its own - these tests just check it renders the comment
 * data it's given, and links to the right profile.
 */

import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { describe, expect, it } from 'vitest';
import Comment from '../../components/Comment';

const renderComment = (comment) => {
  return render(
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Comment comment={comment} />
    </BrowserRouter>
  );
};

const baseComment = {
  id: 42,
  content: 'Great post!',
  author_username: 'mikechen',
  author_display_name: 'Mike Chen',
  author_profile_picture: '/static/uploads/avatars/mike.jpg',
  created_at: '2026-01-15T10:00:00Z',
};

describe('Comment Component', () => {
  it('displays the comment content', () => {
    renderComment(baseComment);
    expect(screen.getByText('Great post!')).toBeInTheDocument();
  });

  it("displays the author's display name and username", () => {
    renderComment(baseComment);
    expect(screen.getByText('Mike Chen')).toBeInTheDocument();
    expect(screen.getByText('@mikechen')).toBeInTheDocument();
  });

  it("links the author's name to their profile", () => {
    renderComment(baseComment);
    // The avatar is also wrapped in a same-named link, so scope to the
    // text link specifically rather than getByRole('link', { name }),
    // which would match both.
    expect(screen.getByText('Mike Chen').closest('a')).toHaveAttribute(
      'href',
      '/profile/mikechen'
    );
  });

  it("links the author's avatar to their profile", () => {
    renderComment(baseComment);
    const avatar = screen.getByAltText('Mike Chen');
    expect(avatar.closest('a')).toHaveAttribute('href', '/profile/mikechen');
  });
});
