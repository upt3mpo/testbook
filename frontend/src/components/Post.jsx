import React, { useEffect, useId, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { postsAPI } from '../api';
import { useAuth } from '../AuthContext';
import { announce } from './LiveRegion';
import './Post.css';

function Post({ post, onDelete, onUpdate, detailed = false }) {
  const { user } = useAuth();
  // useId, not `post-${post.id}-...`: a repost embeds its original, so the same post id can
  // appear twice on one page, and aria-controls needs ids that are unique in the document.
  const uid = useId();
  const dropdownId = `${uid}-menu`;
  const reactionsId = `${uid}-reactions`;
  const [showCommentInput, setShowCommentInput] = useState(false);
  const [commentText, setCommentText] = useState('');
  const [loading, setLoading] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editedContent, setEditedContent] = useState(post.content);
  const [showDropdown, setShowDropdown] = useState(false);
  const [showReactions, setShowReactions] = useState(false);
  // Pointer-only: is the pointer over the reaction picker, and has Escape dismissed the
  // hover-revealed picker? Deliberately separate from showReactions (click/keyboard state)
  // so hover can never fight a click or change aria-expanded.
  const [hoveringReactions, setHoveringReactions] = useState(false);
  const [hoverDismissed, setHoverDismissed] = useState(false);
  const [imageOrientation, setImageOrientation] = useState('square');
  const dropdownRef = useRef(null);
  const reactionsRef = useRef(null);
  const menuButtonRef = useRef(null);
  const reactButtonRef = useRef(null);
  const editTextareaRef = useRef(null);
  const commentButtonRef = useRef(null);
  const commentInputRef = useRef(null);
  const wasEditing = useRef(false);
  const wasCommenting = useRef(false);

  useEffect(() => {
    if (!isEditing) {
      setEditedContent(post.content);
    }
  }, [post, isEditing]);

  const isOwnPost = post.author_id === user?.id;

  // Focus management: when a control opens something, move focus into it; when
  // it closes, put focus back on the control that opened it. Without this,
  // focus falls back to <body> every time the opener unmounts or is hidden.
  useEffect(() => {
    if (isEditing) {
      editTextareaRef.current?.focus();
    } else if (wasEditing.current) {
      menuButtonRef.current?.focus();
    }
    wasEditing.current = isEditing;
  }, [isEditing]);

  useEffect(() => {
    if (showCommentInput) {
      commentInputRef.current?.focus();
    } else if (wasCommenting.current) {
      commentButtonRef.current?.focus();
    }
    wasCommenting.current = showCommentInput;
  }, [showCommentInput]);

  // Escape closes the open menu or reaction picker and returns focus to its trigger. It also
  // dismisses a picker that is only showing because the pointer is hovering (WCAG 1.4.13).
  useEffect(() => {
    if (!showDropdown && !showReactions && !hoveringReactions) return undefined;
    const handleEscape = (event) => {
      if (event.key !== 'Escape') return;
      if (showDropdown) {
        setShowDropdown(false);
        menuButtonRef.current?.focus();
      } else if (showReactions) {
        setShowReactions(false);
        reactButtonRef.current?.focus();
      } else {
        setHoverDismissed(true);
      }
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [showDropdown, showReactions, hoveringReactions]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    };

    if (showDropdown) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => {
        document.removeEventListener('mousedown', handleClickOutside);
      };
    }
  }, [showDropdown]);

  // Close the reaction picker when clicking outside it (it no longer closes on mouse-leave)
  useEffect(() => {
    if (!showReactions) return undefined;
    const handleClickOutside = (event) => {
      if (reactionsRef.current && !reactionsRef.current.contains(event.target)) {
        setShowReactions(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showReactions]);

  const emitUpdate = (updatedPost) => {
    if (onUpdate) {
      onUpdate(updatedPost);
    }
  };

  const handleReaction = async (reactionType) => {
    try {
      if (post.user_reaction === reactionType) {
        const response = await postsAPI.removeReaction(post.id);
        emitUpdate(response.data);
        announce('Reaction removed');
      } else {
        const response = await postsAPI.addReaction(post.id, reactionType);
        emitUpdate(response.data);
        announce(`Reacted with ${reactionType}`);
      }
    } catch (err) {
      console.error('Failed to update reaction:', err);
    } finally {
      setShowReactions(false);
    }
  };

  const handleRepost = async () => {
    try {
      const targetPostId = post.is_repost ? post.original_post_id : post.id;

      if (post.has_reposted) {
        await postsAPI.deleteRepost(targetPostId);
        emitUpdate({
          ...post,
          has_reposted: false,
          reposts_count: Math.max(0, post.reposts_count - 1),
        });
        announce('Repost removed');
      } else {
        await postsAPI.createRepost({ original_post_id: targetPostId, content: '' });
        emitUpdate({
          ...post,
          has_reposted: true,
          reposts_count: post.reposts_count + 1,
        });
        announce('Reposted');
      }
    } catch (err) {
      console.error('Failed to toggle repost:', err);
      alert(`Failed to ${post.has_reposted ? 'remove' : 'create'} repost`);
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
    setEditedContent(post.content);
    setShowDropdown(false);
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setEditedContent(post.content);
  };

  const handleSaveEdit = async () => {
    if (!editedContent.trim()) {
      alert('Post content cannot be empty');
      return;
    }

    try {
      const response = await postsAPI.updatePost(post.id, {
        content: editedContent,
        image_url: post.image_url,
        video_url: post.video_url,
      });
      emitUpdate(response.data);
      setIsEditing(false);
      alert('Post updated successfully!');
    } catch (err) {
      console.error('Failed to update post:', err);
      alert('Failed to update post');
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this post?')) return;
    setShowDropdown(false);

    try {
      await postsAPI.deletePost(post.id);
      // This post (and the focused control inside it) is about to unmount, so
      // park focus on <main> instead of letting it fall back to <body>.
      document.getElementById('main-content')?.focus();
      onDelete(post.id);
      announce('Post deleted');
    } catch (err) {
      console.error('Failed to delete post:', err);
      alert('Failed to delete post');
    }
  };

  const handleComment = async (e) => {
    e.preventDefault();
    if (!commentText.trim()) return;

    setLoading(true);
    try {
      await postsAPI.addComment(post.id, commentText);
      setCommentText('');
      setShowCommentInput(false);
      announce('Comment posted');
      emitUpdate({
        ...post,
        comments_count: post.comments_count + 1,
      });
    } catch (err) {
      console.error('Failed to add comment:', err);
      alert('Failed to add comment');
    } finally {
      setLoading(false);
    }
  };

  const handleImageLoad = (e) => {
    const img = e.target;
    const aspectRatio = img.naturalWidth / img.naturalHeight;

    if (aspectRatio > 1.3) {
      setImageOrientation('horizontal');
    } else if (aspectRatio < 0.8) {
      setImageOrientation('vertical');
    } else {
      setImageOrientation('square');
    }
  };

  const reactions = ['like', 'love', 'haha', 'wow', 'sad', 'angry'];

  const reactionEmojis = {
    like: '👍',
    love: '❤️',
    haha: '😆',
    wow: '😮',
    sad: '😢',
    angry: '😠',
  };

  return (
    <article
      className="post card"
      aria-label={`Post by ${post.author_display_name}`}
      data-testid={`post-${post.id}`}
      data-testid-generic="post-item"
      data-post-id={post.id}
      data-post-author={post.author_username}
      data-is-own-post={isOwnPost}
      data-is-repost={post.is_repost}
    >
      {post.is_repost && (
        <div className="repost-header" data-testid={`repost-indicator-${post.id}`}>
          <span className="text-secondary text-small">
            <span aria-hidden="true">🔁</span> {post.author_display_name} reposted
          </span>
        </div>
      )}

      <div className="post-header">
        <Link to={`/profile/${post.author_username}`} className="post-author-link">
          <img
            src={post.author_profile_picture}
            alt={post.author_display_name}
            className="avatar"
            data-testid={`post-${post.id}-avatar`}
          />
        </Link>
        <div className="post-author-info">
          <Link
            to={`/profile/${post.author_username}`}
            className="post-author-name"
            data-testid={`post-${post.id}-author`}
          >
            {post.author_display_name}
          </Link>
          <span className="post-username text-secondary text-small">@{post.author_username}</span>
          <span
            className="post-time text-secondary text-small"
            data-testid={`post-${post.id}-time`}
          >
            {new Date(post.created_at).toLocaleString()}
          </span>
        </div>
        {isOwnPost && (
          <div className="post-actions-menu" ref={dropdownRef}>
            <button
              ref={menuButtonRef}
              onClick={() => setShowDropdown(!showDropdown)}
              className="btn btn-secondary post-menu-btn"
              aria-label="Post options"
              aria-expanded={showDropdown}
              aria-controls={dropdownId}
              data-testid={`post-${post.id}-menu-button`}
            >
              <span aria-hidden="true">⋯</span>
            </button>
            {showDropdown && (
              <div
                className="post-dropdown"
                id={dropdownId}
                data-testid={`post-${post.id}-dropdown`}
              >
                <button
                  onClick={handleEdit}
                  className="dropdown-item"
                  data-testid={`post-${post.id}-edit-button`}
                >
                  <span aria-hidden="true">✏️</span> Edit
                </button>
                <button
                  onClick={handleDelete}
                  className="dropdown-item dropdown-item-danger"
                  data-testid={`post-${post.id}-delete-button`}
                >
                  <span aria-hidden="true">🗑️</span> Delete
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {isEditing ? (
        <div className="post-edit-form" data-testid={`post-${post.id}-edit-form`}>
          <textarea
            ref={editTextareaRef}
            aria-label="Edit post content"
            className="input post-edit-textarea"
            value={editedContent}
            onChange={(e) => setEditedContent(e.target.value)}
            data-testid={`post-${post.id}-edit-textarea`}
          />
          <div className="post-edit-actions">
            <button
              onClick={handleSaveEdit}
              className="btn btn-primary"
              data-testid={`post-${post.id}-save-button`}
            >
              Save
            </button>
            <button
              onClick={handleCancelEdit}
              className="btn btn-secondary"
              data-testid={`post-${post.id}-cancel-button`}
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="post-content" data-testid={`post-${post.id}-content`}>
          <p>{post.content}</p>
        </div>
      )}

      {post.image_url && (
        <img
          src={post.image_url}
          alt="Post content"
          className={`post-media post-media-${imageOrientation}`}
          onLoad={handleImageLoad}
          data-testid={`post-${post.id}-image`}
          data-image-orientation={imageOrientation}
        />
      )}

      {post.video_url && (
        <video
          src={post.video_url}
          controls
          className="post-media"
          data-testid={`post-${post.id}-video`}
        />
      )}

      {post.is_repost && post.original_post && (
        <div className="original-post" data-testid={`post-${post.id}-original`}>
          <Post post={post.original_post} onDelete={() => {}} onUpdate={() => {}} />
        </div>
      )}

      <div className="post-stats" data-testid={`post-${post.id}-stats`}>
        <span className="text-secondary text-small">{post.reactions_count} reactions</span>
        <span className="text-secondary text-small">{post.comments_count} comments</span>
        <span className="text-secondary text-small">{post.reposts_count} reposts</span>
      </div>

      <div className="post-actions">
        {/* Hover-to-reveal is done in CSS (.reactions-container:hover), not React state.
            React state (showReactions) is only ever set by an explicit click, tap or key
            press, so aria-expanded always matches what the user chose, and a hover can
            neither fight a click nor close a picker a keyboard user opened. */}
        {/* Hover/pointer handlers only: hover-reveal is a pointer enhancement, and the keyboard
            path is the React button inside (aria-expanded). They exist so Escape can dismiss
            a hover-revealed picker without moving the pointer (WCAG 1.4.13). */}
        {/* eslint-disable-next-line jsx-a11y/no-static-element-interactions */}
        <div
          className={`reactions-container ${hoverDismissed ? 'hover-dismissed' : ''}`}
          ref={reactionsRef}
          onMouseEnter={() => setHoveringReactions(true)}
          onMouseLeave={() => {
            setHoveringReactions(false);
            setHoverDismissed(false);
          }}
        >
          <button
            ref={reactButtonRef}
            className="btn btn-secondary"
            aria-expanded={showReactions}
            aria-controls={reactionsId}
            aria-label={
              post.user_reaction ? `Your reaction: ${post.user_reaction}. Change reaction` : 'React'
            }
            data-testid={`post-${post.id}-react-button`}
            onClick={(e) => {
              e.stopPropagation();
              setShowReactions(!showReactions);
            }}
          >
            {post.user_reaction ? `${reactionEmojis[post.user_reaction]} ▼` : 'React ▼'}
          </button>
          <div className={`reactions-dropdown ${showReactions ? 'show' : ''}`} id={reactionsId}>
            {reactions.map((reaction) => (
              <button
                key={reaction}
                onClick={() => handleReaction(reaction)}
                className={`reaction-btn ${post.user_reaction === reaction ? 'active' : ''}`}
                data-testid={`post-${post.id}-reaction-${reaction}`}
                title={reaction}
                aria-label={reaction.charAt(0).toUpperCase() + reaction.slice(1)}
                aria-pressed={post.user_reaction === reaction}
              >
                {reactionEmojis[reaction]}
              </button>
            ))}
          </div>
        </div>

        <button
          ref={commentButtonRef}
          onClick={() => setShowCommentInput(!showCommentInput)}
          aria-expanded={showCommentInput}
          className="btn btn-secondary"
          data-testid={`post-${post.id}-comment-button`}
        >
          Comment
        </button>

        <button
          onClick={handleRepost}
          className={`btn ${post.has_reposted ? 'btn-primary' : 'btn-secondary'}`}
          data-testid={`post-${post.id}-repost-button`}
        >
          {post.has_reposted ? (
            <>
              <span aria-hidden="true">✓</span> Reposted
            </>
          ) : (
            'Repost'
          )}
        </button>

        {!detailed && (
          <Link
            to={`/post/${post.id}`}
            className="btn btn-secondary"
            aria-label={`View post by ${post.author_display_name}`}
            data-testid={`post-${post.id}-view-button`}
          >
            View
          </Link>
        )}
      </div>

      {showCommentInput && (
        <form
          onSubmit={handleComment}
          className="comment-form"
          data-testid={`post-${post.id}-comment-form`}
        >
          <input
            ref={commentInputRef}
            type="text"
            className="input"
            aria-label="Write a comment"
            placeholder="Write a comment..."
            value={commentText}
            onChange={(e) => setCommentText(e.target.value)}
            disabled={loading}
            data-testid={`post-${post.id}-comment-input`}
          />
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading || !commentText.trim()}
            data-testid={`post-${post.id}-comment-submit`}
          >
            {loading ? 'Posting...' : 'Post'}
          </button>
        </form>
      )}
    </article>
  );
}

export default Post;
