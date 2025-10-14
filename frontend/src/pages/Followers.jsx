import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { usersAPI } from '../api';
import { useAuth } from '../AuthContext';
import { broadcastBlockStatusChange } from '../utils/relationshipEvents';
import './Followers.css';

function Followers() {
  const { username } = useParams();
  const { user } = useAuth();
  const [followers, setFollowers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const isOwnPage = user?.username === username;

  useEffect(() => {
    loadFollowers();
  }, [username]);

  const loadFollowers = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await usersAPI.getFollowers(username);
      setFollowers(response.data);
    } catch (err) {
      setError('Failed to load followers');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleBlock = async (followerUsername) => {
    try {
      await usersAPI.blockUser(followerUsername);
      broadcastBlockStatusChange({ username: followerUsername, isBlocked: true });
      // Refresh the list
      await loadFollowers();
    } catch (err) {
      console.error('Failed to block user:', err);
      alert('Failed to block user');
    }
  };

  const handleUnblock = async (followerUsername) => {
    try {
      await usersAPI.unblockUser(followerUsername);
      broadcastBlockStatusChange({ username: followerUsername, isBlocked: false });
      // Refresh the list
      await loadFollowers();
    } catch (err) {
      console.error('Failed to unblock user:', err);
      alert('Failed to unblock user');
    }
  };

  if (loading) {
    return (
      <div className="loading" data-testid="followers-loading">
        Loading followers...
      </div>
    );
  }

  return (
    <div className="followers-container" data-testid="followers-page">
      <div className="followers-header card">
        <h1 className="followers-title">
          {isOwnPage ? 'Your Followers' : `${username}'s Followers`}
        </h1>
        <p className="text-secondary">{followers.length} followers</p>
      </div>

      {error && (
        <div className="error" data-testid="followers-error">
          {error}
        </div>
      )}

      {followers.length === 0 ? (
        <div className="card" data-testid="no-followers">
          <p className="text-secondary text-center">No followers yet.</p>
        </div>
      ) : (
        <div className="followers-list" data-testid="followers-list">
          {followers.map((follower) => (
            <div
              key={follower.id}
              className="user-item card"
              data-testid={`follower-${follower.id}`}
              data-testid-generic="follower-item"
              data-user-id={follower.id}
              data-username={follower.username}
              data-is-blocked={follower.is_blocked}
            >
              <Link to={`/profile/${follower.username}`} className="user-link">
                <img
                  src={follower.profile_picture}
                  alt={follower.display_name}
                  className="avatar"
                  data-testid={`follower-${follower.id}-avatar`}
                />
              </Link>
              <div className="user-info">
                <Link
                  to={`/profile/${follower.username}`}
                  className="user-name"
                  data-testid={`follower-${follower.id}-name`}
                >
                  {follower.display_name}
                </Link>
                <span className="user-username text-secondary text-small">
                  @{follower.username}
                </span>
                {follower.bio && <p className="user-bio text-small">{follower.bio}</p>}
              </div>
              <div className="user-actions">
                {isOwnPage && (
                  <>
                    {follower.is_blocked ? (
                      <button
                        onClick={() => handleUnblock(follower.username)}
                        className="btn btn-secondary"
                        data-testid={`follower-${follower.id}-unblock-button`}
                      >
                        Unblock
                      </button>
                    ) : (
                      <button
                        onClick={() => handleBlock(follower.username)}
                        className="btn btn-danger"
                        data-testid={`follower-${follower.id}-block-button`}
                      >
                        Block
                      </button>
                    )}
                  </>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Followers;
