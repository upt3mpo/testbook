import React, { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import { usersAPI } from '../api';
import './Settings.css';

function Settings() {
  const { user, updateUser, logout } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    display_name: user?.display_name || '',
    bio: user?.bio || '',
    theme: user?.theme || 'light',
    text_density: user?.text_density || 'normal',
  });
  const [loading, setLoading] = useState(false);
  const [uploadingAvatar, setUploadingAvatar] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [avatarPreview, setAvatarPreview] = useState(user?.profile_picture || '');
  const fileInputRef = useRef(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });

    // Apply theme and text density immediately for better UX
    if (name === 'theme') {
      document.documentElement.setAttribute('data-theme', value);
    }
    if (name === 'text_density') {
      document.body.className = `text-density-${value}`;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await usersAPI.updateProfile(formData);
      updateUser(response.data);
      setSuccess('Settings updated successfully!');

      // Apply theme and text density immediately
      document.documentElement.setAttribute('data-theme', formData.theme);
      document.body.className = `text-density-${formData.text_density}`;
    } catch (err) {
      setError('Failed to update settings');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAvatarUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      setError('Please select a valid image file (JPG, PNG, GIF, WebP)');
      return;
    }

    setUploadingAvatar(true);
    setError('');

    try {
      const response = await usersAPI.uploadAvatar(file);
      const updatedUser = { ...user, profile_picture: response.data.url };
      updateUser(updatedUser);
      setAvatarPreview(response.data.url);
      setSuccess('Profile picture updated successfully!');
    } catch (err) {
      setError('Failed to upload profile picture');
      console.error(err);
    } finally {
      setUploadingAvatar(false);
    }
  };

  const handleClearAvatar = async () => {
    if (!window.confirm('Are you sure you want to remove your profile picture?')) return;

    setUploadingAvatar(true);
    setError('');

    try {
      const response = await usersAPI.clearAvatar();
      const updatedUser = { ...user, profile_picture: response.data.profile_picture };
      updateUser(updatedUser);
      setAvatarPreview(response.data.profile_picture);
      setSuccess('Profile picture cleared. Using default avatar.');
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (err) {
      setError('Failed to clear profile picture');
      console.error(err);
    } finally {
      setUploadingAvatar(false);
    }
  };

  const handleDeleteAccount = async () => {
    if (
      !window.confirm('Are you sure you want to delete your account? This action cannot be undone.')
    ) {
      return;
    }

    if (
      !window.confirm(
        'This will permanently delete all your posts, comments, and data. Are you absolutely sure?'
      )
    ) {
      return;
    }

    try {
      await usersAPI.deleteAccount();
      logout();
      alert('Account deleted successfully');
      // Use setTimeout to ensure alert is dismissed before navigation
      setTimeout(() => {
        navigate('/');
      }, 100);
    } catch (err) {
      alert('Failed to delete account');
      console.error(err);
    }
  };

  return (
    <div className="settings-container" data-testid="settings-page">
      <div className="settings-content">
        <h1 className="settings-title" data-testid="settings-title">
          Settings
        </h1>

        <div className="settings-card card">
          <h2 className="settings-section-title">Account Information</h2>
          <div className="settings-info">
            <div className="info-item">
              <span className="info-label">Email:</span>
              <span className="info-value" data-testid="settings-email">
                {user?.email}
              </span>
            </div>
            <div className="info-item">
              <span className="info-label">Username:</span>
              <span className="info-value" data-testid="settings-username">
                @{user?.username}
              </span>
            </div>
          </div>
        </div>

        <div className="settings-card card">
          <h2 className="settings-section-title">Profile Picture</h2>

          {error && (
            <div className="error" data-testid="settings-error">
              {error}
            </div>
          )}
          {success && (
            <div className="success" data-testid="settings-success">
              {success}
            </div>
          )}

          <div className="avatar-section">
            <img
              src={avatarPreview || '/static/images/default-avatar.jpg'}
              alt="Profile"
              className="avatar avatar-lg"
              data-testid="settings-avatar-preview"
            />
            <div className="avatar-actions">
              <input
                ref={fileInputRef}
                type="file"
                accept="image/jpeg,image/jpg,image/png,image/gif,image/webp"
                onChange={handleAvatarUpload}
                style={{ display: 'none' }}
                data-testid="settings-avatar-input"
              />
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="btn btn-primary"
                disabled={uploadingAvatar}
                data-testid="settings-upload-avatar-button"
              >
                {uploadingAvatar ? 'Uploading...' : '📷 Upload Photo'}
              </button>
              <button
                type="button"
                onClick={handleClearAvatar}
                className="btn btn-secondary"
                disabled={
                  uploadingAvatar || user?.profile_picture === '/static/images/default-avatar.jpg'
                }
                data-testid="settings-clear-avatar-button"
              >
                Clear Photo
              </button>
            </div>
          </div>
        </div>

        <div className="settings-card card">
          <h2 className="settings-section-title">Profile Settings</h2>

          <form onSubmit={handleSubmit} className="settings-form" data-testid="settings-form">
            <div className="form-group">
              <label htmlFor="display_name">Display Name</label>
              <input
                type="text"
                id="display_name"
                name="display_name"
                className="input"
                value={formData.display_name}
                onChange={handleChange}
                required
                data-testid="settings-display-name-input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="bio">Bio</label>
              <textarea
                id="bio"
                name="bio"
                className="textarea"
                value={formData.bio}
                onChange={handleChange}
                data-testid="settings-bio-input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="theme">Theme</label>
              <select
                id="theme"
                name="theme"
                className="input"
                value={formData.theme}
                onChange={handleChange}
                data-testid="settings-theme-select"
              >
                <option value="light">Light</option>
                <option value="dark">Dark</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="text_density">Text Density</label>
              <select
                id="text_density"
                name="text_density"
                className="input"
                value={formData.text_density}
                onChange={handleChange}
                data-testid="settings-text-density-select"
              >
                <option value="normal">Normal</option>
                <option value="compact">Compact</option>
              </select>
            </div>

            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
              data-testid="settings-save-button"
            >
              {loading ? 'Saving...' : 'Save Changes'}
            </button>
          </form>
        </div>

        <div className="settings-card card danger-zone">
          <h2 className="settings-section-title">Danger Zone</h2>
          <p className="text-secondary">
            Once you delete your account, there is no going back. Please be certain.
          </p>
          <button
            onClick={handleDeleteAccount}
            className="btn btn-danger"
            data-testid="settings-delete-account-button"
          >
            Delete Account
          </button>
        </div>
      </div>
    </div>
  );
}

export default Settings;
