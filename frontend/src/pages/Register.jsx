import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Alert from '../components/Alert';
import { useAuth } from '../AuthContext';
import useDocumentTitle from '../hooks/useDocumentTitle';
import { getErrorMessage } from '../utils/errors';
import './Auth.css';

function Register() {
  useDocumentTitle('Sign Up');
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    display_name: '',
    password: '',
    bio: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    // Clear error when user starts typing
    if (error) {
      setError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await register(formData);
      // User is now automatically logged in, redirect to feed
      navigate('/');
    } catch (err) {
      setError(getErrorMessage(err, 'Registration failed. Please try again.'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-container" data-testid="register-page">
      <div className="auth-card card">
        <h1 className="auth-title" data-testid="register-title">
          Create Account
        </h1>
        <p className="auth-subtitle">Join Testbook today!</p>

        {error && (
          <Alert focusOnMount data-testid="register-error">
            {error}
          </Alert>
        )}

        <form onSubmit={handleSubmit} className="auth-form" data-testid="register-form">
          <div className="auth-field">
            <label htmlFor="register-email" className="auth-label">
              Email
            </label>
            <input
              id="register-email"
              type="email"
              name="email"
              autoComplete="email"
              className="input"
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
              required
              data-testid="register-email-input"
            />
          </div>
          <div className="auth-field">
            <label htmlFor="register-username" className="auth-label">
              Username (lowercase, no spaces)
            </label>
            <input
              id="register-username"
              type="text"
              name="username"
              autoComplete="username"
              className="input"
              placeholder="Username (lowercase, no spaces)"
              value={formData.username}
              onChange={handleChange}
              required
              data-testid="register-username-input"
            />
          </div>
          <div className="auth-field">
            <label htmlFor="register-display_name" className="auth-label">
              Display Name
            </label>
            <input
              id="register-display_name"
              type="text"
              name="display_name"
              autoComplete="name"
              className="input"
              placeholder="Display Name"
              value={formData.display_name}
              onChange={handleChange}
              required
              data-testid="register-displayname-input"
            />
          </div>
          <div className="auth-field">
            <label htmlFor="register-password" className="auth-label">
              Password
            </label>
            <input
              id="register-password"
              type="password"
              name="password"
              autoComplete="new-password"
              className="input"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              required
              data-testid="register-password-input"
            />
          </div>
          <div className="auth-field">
            <label htmlFor="register-bio" className="auth-label">
              Bio (optional)
            </label>
            <textarea
              id="register-bio"
              name="bio"
              className="textarea"
              placeholder="Bio (optional)"
              value={formData.bio}
              onChange={handleChange}
              data-testid="register-bio-input"
            ></textarea>
          </div>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
            data-testid="register-submit-button"
          >
            {loading ? 'Creating Account...' : 'Sign Up'}
          </button>
        </form>

        <div className="auth-divider"></div>

        <Link to="/login" className="btn btn-secondary" data-testid="back-to-login-button">
          Already have an account? Log In
        </Link>
      </div>
    </main>
  );
}

export default Register;
