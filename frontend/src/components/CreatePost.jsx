import React, { useRef, useState } from 'react';
import { postsAPI } from '../api';
import './CreatePost.css';

function CreatePost({ onPostCreated }) {
  const [content, setContent] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileSelect = (file) => {
    if (!file) return;

    // Validate file type
    const validImageTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    const validVideoTypes = ['video/mp4', 'video/mov', 'video/avi'];
    const isValid = [...validImageTypes, ...validVideoTypes].includes(file.type);

    if (!isValid) {
      setError('Please select a valid image (JPG, PNG, GIF, WebP) or video (MP4, MOV, AVI) file');
      return;
    }

    setSelectedFile(file);
    setError('');

    // Create preview URL
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
  };

  const handleFileInputChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const removeFile = () => {
    setSelectedFile(null);
    setPreviewUrl('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!content.trim()) return;

    setLoading(true);
    setError('');

    try {
      let mediaUrl = null;

      // Upload file if selected
      if (selectedFile) {
        setUploading(true);
        const uploadResponse = await postsAPI.uploadMedia(selectedFile);
        mediaUrl = uploadResponse.data.url;
        setUploading(false);
      }

      // Determine if it's an image or video
      const postData = {
        content,
        image_url: selectedFile && selectedFile.type.startsWith('image/') ? mediaUrl : null,
        video_url: selectedFile && selectedFile.type.startsWith('video/') ? mediaUrl : null,
      };

      const response = await postsAPI.createPost(postData);
      onPostCreated(response.data);

      // Reset form
      setContent('');
      setSelectedFile(null);
      setPreviewUrl('');
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (err) {
      setError('Failed to create post');
      console.error(err);
    } finally {
      setLoading(false);
      setUploading(false);
    }
  };

  return (
    <div className="create-post card" data-testid="create-post">
      <form onSubmit={handleSubmit}>
        <textarea
          className="textarea"
          placeholder="What's on your mind?"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          disabled={loading}
          data-testid="create-post-textarea"
        />

        {/* Drag and drop zone */}
        {!selectedFile && (
          <div
            className={`drop-zone ${isDragging ? 'drop-zone-active' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            data-testid="create-post-drop-zone"
          >
            <div className="drop-zone-content">
              <span className="drop-zone-icon">📁</span>
              <p className="drop-zone-text">
                {isDragging ? 'Drop your file here' : 'Click to upload or drag and drop'}
              </p>
              <p className="drop-zone-hint text-small text-secondary">
                Images (JPG, PNG, GIF, WebP) or Videos (MP4, MOV, AVI)
              </p>
            </div>
          </div>
        )}

        {/* Hidden file input */}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/jpeg,image/jpg,image/png,image/gif,image/webp,video/mp4,video/mov,video/avi"
          onChange={handleFileInputChange}
          style={{ display: 'none' }}
          data-testid="create-post-file-input"
        />

        {/* File preview */}
        {selectedFile && (
          <div className="file-preview" data-testid="create-post-preview">
            {selectedFile.type.startsWith('image/') ? (
              <img src={previewUrl} alt="Preview" className="preview-image" />
            ) : (
              <video src={previewUrl} controls className="preview-video" />
            )}
            <button
              type="button"
              className="btn btn-danger remove-file-btn"
              onClick={removeFile}
              disabled={loading}
              data-testid="create-post-remove-file"
            >
              ✕ Remove
            </button>
          </div>
        )}

        {error && <div className="error text-small">{error}</div>}

        <div className="create-post-actions">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => fileInputRef.current?.click()}
            disabled={loading}
            data-testid="create-post-media-button"
          >
            📷 {selectedFile ? 'Change' : 'Add'} Media
          </button>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading || !content.trim()}
            data-testid="create-post-submit-button"
          >
            {uploading ? 'Uploading...' : loading ? 'Posting...' : 'Post'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default CreatePost;
