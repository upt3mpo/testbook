import React, { Suspense, useEffect, useRef } from 'react';
import { Navigate, Route, BrowserRouter as Router, Routes, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './AuthContext';

// Pages
import Feed from './pages/Feed';
import Followers from './pages/Followers';
import Following from './pages/Following';
import Login from './pages/Login';
import PostDetail from './pages/PostDetail';
import Profile from './pages/Profile';
import Register from './pages/Register';
import Settings from './pages/Settings';

// Components
import LiveRegion, { announce } from './components/LiveRegion';
import ErrorBoundary from './components/ErrorBoundary';
import Navbar from './components/Navbar';

// Loading component
function LoadingSpinner() {
  return (
    <div
      className="loading-container"
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
      }}
    >
      <div className="loading" data-testid="loading-spinner">
        Loading...
      </div>
    </div>
  );
}

function PrivateRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner />;
  }

  return isAuthenticated ? children : <Navigate to="/login" />;
}

function PrivateLayout({ children }) {
  // A plain #hash link would work, but moving focus too means the next Tab
  // starts inside the content instead of back in the navbar.
  const skipToContent = (event) => {
    event.preventDefault();
    document.getElementById('main-content')?.focus();
  };

  return (
    <>
      <a href="#main-content" className="skip-link" onClick={skipToContent}>
        Skip to main content
      </a>
      <Navbar />
      <main id="main-content" tabIndex={-1}>
        {children}
      </main>
    </>
  );
}

// A single-page app never reloads, so screen readers get no "new page" cue.
// Announce the new page title after each client-side navigation (skipping the
// initial load, which the browser already announces).
function RouteAnnouncer() {
  const { pathname } = useLocation();
  const isFirstRender = useRef(true);

  useEffect(() => {
    if (isFirstRender.current) {
      isFirstRender.current = false;
      return;
    }
    // Pages set document.title in their own effects; wait a tick so we read the new one.
    const timer = setTimeout(() => announce(document.title), 100);
    return () => clearTimeout(timer);
  }, [pathname]);

  return null;
}

function AppContent() {
  const { user } = useAuth();

  useEffect(() => {
    // Apply theme and text density
    if (user) {
      document.documentElement.setAttribute('data-theme', user.theme || 'light');
      document.body.className = `text-density-${user.text_density || 'normal'}`;
    }
  }, [user]);

  return (
    <div className="app" data-testid="app">
      <LiveRegion />
      <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <RouteAnnouncer />
        <Suspense fallback={<LoadingSpinner />}>
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Protected routes with layout */}
            <Route
              path="/"
              element={
                <PrivateRoute>
                  <PrivateLayout>
                    <Feed />
                  </PrivateLayout>
                </PrivateRoute>
              }
            />
            <Route
              path="/post/:postId"
              element={
                <PrivateRoute>
                  <PrivateLayout>
                    <PostDetail />
                  </PrivateLayout>
                </PrivateRoute>
              }
            />
            <Route
              path="/profile/:username"
              element={
                <PrivateRoute>
                  <PrivateLayout>
                    <Profile />
                  </PrivateLayout>
                </PrivateRoute>
              }
            />
            <Route
              path="/profile/:username/followers"
              element={
                <PrivateRoute>
                  <PrivateLayout>
                    <Followers />
                  </PrivateLayout>
                </PrivateRoute>
              }
            />
            <Route
              path="/profile/:username/following"
              element={
                <PrivateRoute>
                  <PrivateLayout>
                    <Following />
                  </PrivateLayout>
                </PrivateRoute>
              }
            />
            <Route
              path="/settings"
              element={
                <PrivateRoute>
                  <PrivateLayout>
                    <Settings />
                  </PrivateLayout>
                </PrivateRoute>
              }
            />
          </Routes>
        </Suspense>
      </Router>
    </div>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </ErrorBoundary>
  );
}

export default App;
