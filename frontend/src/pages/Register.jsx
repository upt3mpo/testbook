import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import './Auth.css';

function Register() {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    display_name: '',
    password: '',
    bio: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
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
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container" data-testid="register-page">
      <div className="auth-card card">
        <h1 className="auth-title" data-testid="register-title">Create Account</h1>
        <p className="auth-subtitle">Join Testbook today!</p>

        {error && <div className="error" data-testid="register-error">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form" data-testid="register-form">
          <input
            type="email"
            name="email"
            className="input"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            required
            data-testid="register-email-input"
          />
          <input
            type="text"
            name="username"
            className="input"
            placeholder="Username (lowercase, no spaces)"
            value={formData.username}
            onChange={handleChange}
            required
            data-testid="register-username-input"
          />
          <input
            type="text"
            name="display_name"
            className="input"
            placeholder="Display Name"
            value={formData.display_name}
            onChange={handleChange}
            required
            data-testid="register-displayname-input"
          />
          <input
            type="password"
            name="password"
            className="input"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
            data-testid="register-password-input"
          />
          <textarea
            name="bio"
            className="textarea"
            placeholder="Bio (optional)"
            value={formData.bio}
            onChange={handleChange}
            data-testid="register-bio-input"
          ></textarea>
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

        <Link to="/login">
          <button className="btn btn-secondary" data-testid="back-to-login-button">
            Already have an account? Log In
          </button>
        </Link>
      </div>
    </div>
  );
}

export default Register;

