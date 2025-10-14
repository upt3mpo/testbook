import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { usersAPI } from '../api';
import { useAuth } from '../AuthContext';
import './Following.css';

function Following() {
  const { username } = useParams();
  const { user } = useAuth();
  const [following, setFollowing] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const isOwnPage = user?.username === username;

  useEffect(() => {
    loadFollowing();
  }, [username]);

  const loadFollowing = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await usersAPI.getFollowing(username);
      setFollowing(response.data);
    } catch (err) {
      setError('Failed to load following');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleUnfollow = async (followingUsername) => {
    try {
      await usersAPI.unfollowUser(followingUsername);
      // Refresh the list
      loadFollowing();
    } catch (err) {
      console.error('Failed to unfollow user:', err);
      alert('Failed to unfollow user');
    }
  };

  // Note: handleFollow function removed as it's not used in this component
  // Users can only unfollow from the Following page

  if (loading) {
    return (
      <div className="loading" data-testid="following-loading">
        Loading following...
      </div>
    );
  }

  return (
    <div className="following-container" data-testid="following-page">
      <div className="following-header card">
        <h1 className="following-title">{isOwnPage ? 'Following' : `${username} is Following`}</h1>
        <p className="text-secondary">{following.length} following</p>
      </div>

      {error && (
        <div className="error" data-testid="following-error">
          {error}
        </div>
      )}

      {following.length === 0 ? (
        <div className="card" data-testid="no-following">
          <p className="text-secondary text-center">Not following anyone yet.</p>
        </div>
      ) : (
        <div className="following-list" data-testid="following-list">
          {following.map((followedUser) => (
            <div
              key={followedUser.id}
              className="user-item card"
              data-testid={`following-${followedUser.id}`}
              data-testid-generic="following-item"
              data-user-id={followedUser.id}
              data-username={followedUser.username}
              data-is-following={followedUser.is_following}
            >
              <Link to={`/profile/${followedUser.username}`} className="user-link">
                <img
                  src={followedUser.profile_picture}
                  alt={followedUser.display_name}
                  className="avatar"
                  data-testid={`following-${followedUser.id}-avatar`}
                />
              </Link>
              <div className="user-info">
                <Link
                  to={`/profile/${followedUser.username}`}
                  className="user-name"
                  data-testid={`following-${followedUser.id}-name`}
                >
                  {followedUser.display_name}
                </Link>
                <span className="user-username text-secondary text-small">
                  @{followedUser.username}
                </span>
                {followedUser.bio && <p className="user-bio text-small">{followedUser.bio}</p>}
              </div>
              <div className="user-actions">
                {isOwnPage && (
                  <button
                    onClick={() => handleUnfollow(followedUser.username)}
                    className="btn btn-secondary"
                    data-testid={`following-${followedUser.id}-unfollow-button`}
                  >
                    Unfollow
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Following;
