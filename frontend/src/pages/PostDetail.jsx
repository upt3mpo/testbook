import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { postsAPI } from '../api';
import Comment from '../components/Comment';
import Post from '../components/Post';
import './PostDetail.css';

function PostDetail() {
  const { postId } = useParams();
  const navigate = useNavigate();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const reactionEmojis = {
    like: '👍',
    love: '❤️',
    haha: '😆',
    wow: '😮',
    sad: '😢',
    angry: '😠',
  };

  useEffect(() => {
    loadPost();
  }, [postId]);

  const loadPost = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await postsAPI.getPost(postId);
      setPost(response.data);
    } catch (err) {
      setError('Failed to load post');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handlePostDeleted = () => {
    navigate('/');
  };

  const handlePostUpdated = (updatedPost) => {
    setPost((prev) => {
      if (!prev) {
        return updatedPost;
      }

      return {
        ...prev,
        ...updatedPost,
        comments: updatedPost.comments ?? prev.comments,
        reactions: updatedPost.reactions ?? prev.reactions,
      };
    });
  };

  if (loading) {
    return (
      <div className="loading" data-testid="post-detail-loading">
        Loading post...
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="post-detail-container">
        <div className="error" data-testid="post-detail-error">
          {error || 'Post not found'}
        </div>
      </div>
    );
  }

  return (
    <div className="post-detail-container" data-testid="post-detail-page">
      <div className="post-detail-content">
        <Post
          post={post}
          onDelete={handlePostDeleted}
          onUpdate={handlePostUpdated}
          detailed={true}
        />

        <div className="comments-section card" data-testid="comments-section">
          <h3 className="comments-title">Comments ({post.comments?.length || 0})</h3>
          {post.comments && post.comments.length > 0 ? (
            <div className="comments-list" data-testid="comments-list">
              {post.comments.map((comment) => (
                <Comment key={comment.id} comment={comment} />
              ))}
            </div>
          ) : (
            <p className="text-secondary text-small" data-testid="no-comments">
              No comments yet. Be the first to comment!
            </p>
          )}
        </div>

        <div className="reactions-section card" data-testid="reactions-section">
          <h3 className="reactions-title">Reactions ({post.reactions?.length || 0})</h3>
          {post.reactions && post.reactions.length > 0 ? (
            <div className="reactions-list" data-testid="reactions-list">
              {post.reactions.map((reaction) => (
                <div
                  key={reaction.id}
                  className="reaction-item"
                  data-testid={`reaction-${reaction.id}`}
                  data-testid-generic="reaction-item"
                  data-reaction-type={reaction.reaction_type}
                  data-user={reaction.username}
                >
                  <span className="reaction-emoji" title={reaction.reaction_type}>
                    {reactionEmojis[reaction.reaction_type]}
                  </span>
                  <span className="reaction-user">{reaction.display_name}</span>
                  <span className="reaction-username text-secondary text-small">
                    @{reaction.username}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-secondary text-small" data-testid="no-reactions">
              No reactions yet.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default PostDetail;
