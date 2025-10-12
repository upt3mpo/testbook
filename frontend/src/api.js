import axios from 'axios';

const API_URL = '/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auth API
export const authAPI = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (userData) => api.post('/auth/register', userData),
  getMe: () => api.get('/auth/me'),
};

// Users API
export const usersAPI = {
  getProfile: (username) => api.get(`/users/${username}`),
  updateProfile: (data) => api.put('/users/me', data),
  uploadAvatar: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/users/me/upload-avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  clearAvatar: () => api.put('/users/me', { profile_picture: '' }),
  deleteAccount: () => api.delete('/users/me'),
  followUser: (username) => api.post(`/users/${username}/follow`),
  unfollowUser: (username) => api.delete(`/users/${username}/follow`),
  blockUser: (username) => api.post(`/users/${username}/block`),
  unblockUser: (username) => api.delete(`/users/${username}/block`),
  getUserPosts: (username, skip = 0, limit = 50) =>
    api.get(`/users/${username}/posts?skip=${skip}&limit=${limit}`),
  getFollowers: (username) => api.get(`/users/${username}/followers`),
  getFollowing: (username) => api.get(`/users/${username}/following`),
};

// Posts API
export const postsAPI = {
  createPost: (data) => api.post('/posts/', data),
  updatePost: (postId, data) => api.put(`/posts/${postId}`, data),
  createRepost: (data) => api.post('/posts/repost', data),
  deleteRepost: (postId) => api.delete(`/posts/repost/${postId}`),
  deletePost: (postId) => api.delete(`/posts/${postId}`),
  getPost: (postId) => api.get(`/posts/${postId}`),
  addComment: (postId, content) => api.post(`/posts/${postId}/comments`, { content }),
  addReaction: (postId, reactionType) => api.post(`/posts/${postId}/reactions`, { reaction_type: reactionType }),
  removeReaction: (postId) => api.delete(`/posts/${postId}/reactions`),
  uploadMedia: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/posts/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};

// Feed API
export const feedAPI = {
  getAllFeed: (skip = 0, limit = 50) => api.get(`/feed/all?skip=${skip}&limit=${limit}`),
  getFollowingFeed: (skip = 0, limit = 50) => api.get(`/feed/following?skip=${skip}&limit=${limit}`),
};

// Dev API
export const devAPI = {
  resetDatabase: () => api.post('/dev/reset'),
  seedDatabase: () => api.post('/dev/seed'),
  getAllUsers: () => api.get('/dev/users'),
  createTestPost: (userId, content, imageUrl = null, videoUrl = null) =>
    api.post('/dev/create-post', { user_id: userId, content, image_url: imageUrl, video_url: videoUrl }),
};

export default api;

