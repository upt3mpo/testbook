import React, { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { postsAPI } from '../api';
import { useAuth } from '../AuthContext';
import './Post.css';

function Post({ post, onDelete, onUpdate, detailed = false }) {
  const { user } = useAuth();
  const [showCommentInput, setShowCommentInput] = useState(false);
  const [commentText, setCommentText] = useState('');
  const [loading, setLoading] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editedContent, setEditedContent] = useState(post.content);
  const [showDropdown, setShowDropdown] = useState(false);
  const [showReactions, setShowReactions] = useState(false);
  const [imageOrientation, setImageOrientation] = useState('square');
  const dropdownRef = useRef(null);

  useEffect(() => {
    if (!isEditing) {
      setEditedContent(post.content);
    }
  }, [post, isEditing]);

  const isOwnPost = post.author_id === user?.id;

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
      } else {
        const response = await postsAPI.addReaction(post.id, reactionType);
        emitUpdate(response.data);
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
      } else {
        await postsAPI.createRepost({ original_post_id: targetPostId, content: '' });
        emitUpdate({
          ...post,
          has_reposted: true,
          reposts_count: post.reposts_count + 1,
        });
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
      onDelete(post.id);
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
    <div
      className="post card"
      data-testid={`post-${post.id}`}
      data-testid-generic="post-item"
      data-post-id={post.id}
      data-post-author={post.author_username}
      data-is-own-post={isOwnPost}
      data-is-repost={post.is_repost}
    >
      {post.is_repost && (
        <div className="repost-header" data-testid={`repost-indicator-${post.id}`}>
          <span className="text-secondary text-small">🔁 {post.author_display_name} reposted</span>
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
              onClick={() => setShowDropdown(!showDropdown)}
              className="btn btn-secondary post-menu-btn"
              data-testid={`post-${post.id}-menu-button`}
            >
              ⋯
            </button>
            {showDropdown && (
              <div className="post-dropdown" data-testid={`post-${post.id}-dropdown`}>
                <button
                  onClick={handleEdit}
                  className="dropdown-item"
                  data-testid={`post-${post.id}-edit-button`}
                >
                  ✏️ Edit
                </button>
                <button
                  onClick={handleDelete}
                  className="dropdown-item dropdown-item-danger"
                  data-testid={`post-${post.id}-delete-button`}
                >
                  🗑️ Delete
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {isEditing ? (
        <div className="post-edit-form" data-testid={`post-${post.id}-edit-form`}>
          <textarea
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
        <div
          className="reactions-container"
          onMouseEnter={() => setShowReactions(true)}
          onMouseLeave={() => setShowReactions(false)}
        >
          <button
            className="btn btn-secondary"
            data-testid={`post-${post.id}-react-button`}
            onClick={(e) => {
              e.stopPropagation();
              setShowReactions(!showReactions);
            }}
          >
            {post.user_reaction ? `${reactionEmojis[post.user_reaction]} ▼` : 'React ▼'}
          </button>
          <div className={`reactions-dropdown ${showReactions ? 'show' : ''}`}>
            {reactions.map((reaction) => (
              <button
                key={reaction}
                onClick={() => handleReaction(reaction)}
                className={`reaction-btn ${post.user_reaction === reaction ? 'active' : ''}`}
                data-testid={`post-${post.id}-reaction-${reaction}`}
                title={reaction}
              >
                {reactionEmojis[reaction]}
              </button>
            ))}
          </div>
        </div>

        <button
          onClick={() => setShowCommentInput(!showCommentInput)}
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
          {post.has_reposted ? '✓ Reposted' : 'Repost'}
        </button>

        {!detailed && (
          <Link to={`/post/${post.id}`}>
            <button className="btn btn-secondary" data-testid={`post-${post.id}-view-button`}>
              View
            </button>
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
            type="text"
            className="input"
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
    </div>
  );
}

export default Post;
