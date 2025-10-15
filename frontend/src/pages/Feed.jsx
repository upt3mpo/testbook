import React, { useCallback, useEffect, useRef, useState } from 'react';
import { feedAPI } from '../api';
import CreatePost from '../components/CreatePost';
import Post from '../components/Post';
import { BLOCK_EVENT_STORAGE_KEY, BLOCK_STATUS_EVENT } from '../utils/relationshipEvents';
import './Feed.css';

function Feed() {
  const [feedType, setFeedType] = useState('all'); // 'all' or 'following'
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const lastLoadedRef = useRef(0);

  const loadFeed = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const response =
        feedType === 'all' ? await feedAPI.getAllFeed() : await feedAPI.getFollowingFeed();
      setPosts(response.data);
      lastLoadedRef.current = Date.now();
    } catch (err) {
      setError('Failed to load feed');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [feedType]);

  useEffect(() => {
    loadFeed();
  }, [loadFeed]);

  // Reload feed when returning to page (e.g., after blocking someone)
  useEffect(() => {
    if (typeof window === 'undefined') {
      return;
    }

    const handleFocus = () => {
      loadFeed();
    };

    window.addEventListener('focus', handleFocus);

    return () => {
      window.removeEventListener('focus', handleFocus);
    };
  }, [loadFeed]);

  // Listen for explicit relationship changes (block/unblock) to refresh feed data.
  useEffect(() => {
    if (typeof window === 'undefined') {
      return;
    }

    const handleBlockChange = () => {
      loadFeed();
    };

    window.addEventListener(BLOCK_STATUS_EVENT, handleBlockChange);
    return () => {
      window.removeEventListener(BLOCK_STATUS_EVENT, handleBlockChange);
    };
  }, [loadFeed]);

  // If a block event happened while the feed was unmounted, ensure we refresh on mount.
  useEffect(() => {
    if (typeof window === 'undefined') {
      return;
    }

    try {
      const lastBlockChange = Number(window.localStorage.getItem(BLOCK_EVENT_STORAGE_KEY) || 0);

      if (lastBlockChange && lastBlockChange > lastLoadedRef.current) {
        loadFeed();
      }
    } catch (err) {
      console.warn('Failed to read block status timestamp', err);
    }
  }, [loadFeed]);

  const handlePostCreated = useCallback((newPost) => {
    setPosts((prevPosts) => [newPost, ...prevPosts]);
  }, []);

  const handlePostDeleted = useCallback((postId) => {
    setPosts((prevPosts) => prevPosts.filter((post) => post.id !== postId));
  }, []);

  const handlePostUpdated = useCallback((updatedPost) => {
    setPosts((prevPosts) =>
      prevPosts.map((post) => (post.id === updatedPost.id ? updatedPost : post))
    );
  }, []);

  return (
    <div className="feed-container" data-testid="feed-page">
      <div className="feed-content">
        <div className="feed-tabs" data-testid="feed-tabs">
          <button
            className={`feed-tab ${feedType === 'all' ? 'active' : ''}`}
            onClick={() => setFeedType('all')}
            data-testid="feed-tab-all"
          >
            See All
          </button>
          <button
            className={`feed-tab ${feedType === 'following' ? 'active' : ''}`}
            onClick={() => setFeedType('following')}
            data-testid="feed-tab-following"
          >
            Following
          </button>
        </div>

        <CreatePost onPostCreated={handlePostCreated} />

        {error && (
          <div className="error" data-testid="feed-error">
            {error}
          </div>
        )}

        {loading ? (
          <div className="loading" data-testid="feed-loading">
            Loading posts...
          </div>
        ) : posts.length === 0 ? (
          <div className="empty-feed card" data-testid="feed-empty">
            <p>
              No posts to show.{' '}
              {feedType === 'following' ? 'Try following some users!' : 'Be the first to post!'}
            </p>
          </div>
        ) : (
          <div className="posts-list" data-testid="posts-list">
            {posts.map((post) => (
              <Post
                key={post.id}
                post={post}
                onDelete={handlePostDeleted}
                onUpdate={handlePostUpdated}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Feed;
