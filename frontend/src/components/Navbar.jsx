import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import './Navbar.css';

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar" data-testid="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo" data-testid="navbar-logo">
          <h2>Testbook</h2>
        </Link>

        {user ? (
          // Authenticated menu
          <>
            <div className="navbar-menu">
              <Link to="/" className="navbar-link" data-testid="navbar-home-link">
                Home
              </Link>
              <Link
                to={`/profile/${user.username}`}
                className="navbar-link"
                data-testid="navbar-profile-link"
              >
                Profile
              </Link>
              <Link to="/settings" className="navbar-link" data-testid="navbar-settings-link">
                Settings
              </Link>
              <button
                onClick={handleLogout}
                className="btn btn-secondary navbar-logout"
                data-testid="navbar-logout-button"
              >
                Logout
              </button>
            </div>

            <div className="navbar-user" data-testid="navbar-user-info">
              <div data-testid="user-menu">
                <img
                  src={user.profile_picture || '/static/images/default-avatar.jpg'}
                  alt={user.display_name}
                  className="avatar avatar-sm"
                  data-testid="navbar-user-avatar"
                />
                <span className="navbar-username" data-testid="navbar-username">
                  {user.display_name}
                </span>
              </div>
            </div>
          </>
        ) : (
          // Unauthenticated menu
          <div className="navbar-menu">
            <Link to="/login" className="navbar-link" data-testid="navbar-login-link">
              Login
            </Link>
            <Link to="/register" className="navbar-link" data-testid="navbar-register-link">
              Register
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
