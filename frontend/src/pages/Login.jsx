import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Alert from '../components/Alert';
import { useAuth } from '../AuthContext';
import useDocumentTitle from '../hooks/useDocumentTitle';
import { getErrorMessage } from '../utils/errors';
import './Auth.css';

function Login() {
  useDocumentTitle('Log In');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(email, password);
      navigate('/');
    } catch (err) {
      setError(getErrorMessage(err, 'Invalid credentials. Please check your email and password.'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-container" data-testid="login-page">
      <div className="auth-card card">
        <h1 className="auth-title" data-testid="login-title">
          Testbook
        </h1>
        <p className="auth-subtitle">Connect with friends and practice testing!</p>

        {error && (
          <Alert focusOnMount data-testid="login-error">
            {error}
          </Alert>
        )}

        <form onSubmit={handleSubmit} className="auth-form" data-testid="login-form">
          <label htmlFor="login-email" className="sr-only">
            Email
          </label>
          <input
            id="login-email"
            type="email"
            autoComplete="username"
            className="input"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            data-testid="login-email-input"
          />
          <label htmlFor="login-password" className="sr-only">
            Password
          </label>
          <input
            id="login-password"
            type="password"
            autoComplete="current-password"
            className="input"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            data-testid="login-password-input"
          />
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
            data-testid="login-submit-button"
          >
            {loading ? 'Logging in...' : 'Log In'}
          </button>
        </form>

        <div className="auth-divider"></div>

        <Link to="/register" className="btn btn-secondary" data-testid="create-account-button">
          Create New Account
        </Link>

        <div className="auth-hint">
          <p className="text-small text-secondary">Test Accounts:</p>
          <p className="text-small text-secondary">sarah.johnson@testbook.com / Sarah2024!</p>
          <p className="text-small text-secondary">mike.chen@testbook.com / MikeRocks88</p>
        </div>
      </div>
    </main>
  );
}

export default Login;
