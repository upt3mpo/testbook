import React from 'react';
import { Link } from 'react-router-dom';
import './Comment.css';

function Comment({ comment }) {
  return (
    <div
      className="comment"
      data-testid={`comment-${comment.id}`}
      data-testid-generic="comment-item"
      data-comment-id={comment.id}
      data-author={comment.author_username}
    >
      <Link to={`/profile/${comment.author_username}`}>
        <img
          src={comment.author_profile_picture}
          alt={comment.author_display_name}
          className="avatar avatar-sm"
          data-testid={`comment-${comment.id}-avatar`}
        />
      </Link>
      <div className="comment-body">
        <div className="comment-header">
          <Link to={`/profile/${comment.author_username}`} className="comment-author" data-testid={`comment-${comment.id}-author`}>
            {comment.author_display_name}
          </Link>
          <span className="comment-username text-secondary text-small">@{comment.author_username}</span>
          <span className="comment-time text-secondary text-small" data-testid={`comment-${comment.id}-time`}>
            {new Date(comment.created_at).toLocaleString()}
          </span>
        </div>
        <div className="comment-content" data-testid={`comment-${comment.id}-content`}>
          {comment.content}
        </div>
      </div>
    </div>
  );
}

export default Comment;

