import React, { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { usersAPI } from '../api';
import { useAuth } from '../AuthContext';
import Post from '../components/Post';
import { broadcastBlockStatusChange } from '../utils/relationshipEvents';
import './Profile.css';

function Profile() {
  const { username } = useParams();
  const navigate = useNavigate();
  const { user: currentUser } = useAuth();
  const [profile, setProfile] = useState(null);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const isOwnProfile = currentUser?.username === username;

  useEffect(() => {
    loadProfile();
    loadPosts();
  }, [username]);

  const loadProfile = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await usersAPI.getProfile(username);
      setProfile(response.data);
    } catch (err) {
      setError('Failed to load profile');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadPosts = async () => {
    try {
      const response = await usersAPI.getUserPosts(username);
      setPosts(response.data);
    } catch (err) {
      console.error('Failed to load posts:', err);
    }
  };

  const handleFollow = async () => {
    try {
      if (profile.is_following) {
        await usersAPI.unfollowUser(username);
        setProfile({
          ...profile,
          is_following: false,
          followers_count: profile.followers_count - 1,
        });
      } else {
        await usersAPI.followUser(username);
        setProfile({
          ...profile,
          is_following: true,
          followers_count: profile.followers_count + 1,
        });
      }
    } catch (err) {
      console.error('Failed to update follow status:', err);
      alert('Failed to update follow status');
    }
  };

  const handleBlock = async () => {
    if (
      !window.confirm(
        `Are you sure you want to ${profile.is_blocked ? 'unblock' : 'block'} this user?`
      )
    )
      return;

    try {
      if (profile.is_blocked) {
        await usersAPI.unblockUser(username);
        setProfile((prev) => (prev ? { ...prev, is_blocked: false } : prev));
        broadcastBlockStatusChange({ username, isBlocked: false });
      } else {
        await usersAPI.blockUser(username);
        setProfile((prev) => (prev ? { ...prev, is_blocked: true, is_following: false } : prev));
        broadcastBlockStatusChange({ username, isBlocked: true });
      }
    } catch (err) {
      console.error('Failed to update block status:', err);
      alert('Failed to update block status');
    }
  };

  const handlePostDeleted = (postId) => {
    setPosts((prevPosts) => prevPosts.filter((post) => post.id !== postId));
  };

  const handlePostUpdated = (updatedPost) => {
    setPosts((prevPosts) =>
      prevPosts.map((post) => (post.id === updatedPost.id ? updatedPost : post))
    );
  };

  if (loading) {
    return (
      <div className="loading" data-testid="profile-loading">
        Loading profile...
      </div>
    );
  }

  if (error || !profile) {
    return (
      <div className="profile-container">
        <div className="error" data-testid="profile-error">
          {error || 'Profile not found'}
        </div>
      </div>
    );
  }

  return (
    <div className="profile-container" data-testid="profile-page">
      <div className="profile-content">
        <div className="profile-header card" data-testid="profile-header">
          <div className="profile-info">
            <img
              src={profile.profile_picture}
              alt={profile.display_name}
              className="avatar avatar-lg"
              data-testid="profile-avatar"
            />
            <div className="profile-details">
              <h2 className="profile-name" data-testid="profile-display-name">
                {profile.display_name}
              </h2>
              <p className="profile-username text-secondary" data-testid="profile-username">
                @{profile.username}
              </p>
              {profile.bio && (
                <p className="profile-bio" data-testid="profile-bio">
                  {profile.bio}
                </p>
              )}
              <div className="profile-stats">
                <span data-testid="profile-posts-count">
                  <strong>{profile.posts_count}</strong> posts
                </span>
                <Link
                  to={`/profile/${username}/followers`}
                  className="profile-stat-link"
                  data-testid="profile-followers-link"
                >
                  <strong>{profile.followers_count}</strong> followers
                </Link>
                <Link
                  to={`/profile/${username}/following`}
                  className="profile-stat-link"
                  data-testid="profile-following-link"
                >
                  <strong>{profile.following_count}</strong> following
                </Link>
              </div>
            </div>
          </div>

          {isOwnProfile ? (
            <div className="profile-actions">
              <button
                onClick={() => navigate('/settings')}
                className="btn btn-primary"
                data-testid="profile-edit-button"
              >
                ✏️ Edit Profile
              </button>
            </div>
          ) : (
            <div className="profile-actions">
              <button
                onClick={handleFollow}
                className={`btn ${profile.is_following ? 'btn-secondary' : 'btn-primary'}`}
                data-testid="profile-follow-button"
              >
                {profile.is_following ? 'Unfollow' : 'Follow'}
              </button>
              <button
                onClick={handleBlock}
                className="btn btn-danger"
                data-testid="profile-block-button"
              >
                {profile.is_blocked ? 'Unblock' : 'Block'}
              </button>
            </div>
          )}
        </div>

        <div className="profile-posts">
          <h3 className="posts-title">Posts</h3>
          {posts.length === 0 ? (
            <div className="empty-posts card" data-testid="profile-no-posts">
              <p className="text-secondary">No posts yet.</p>
            </div>
          ) : (
            <div className="posts-list" data-testid="profile-posts-list">
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
    </div>
  );
}

export default Profile;
