import React, { Suspense, useEffect } from 'react';
import { Navigate, Route, BrowserRouter as Router, Routes } from 'react-router-dom';
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
  return (
    <>
      <Navbar />
      {children}
    </>
  );
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
      <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
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
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
