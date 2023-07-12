import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import api from '../api';

const PostCreate = () => {
  const [text, setText] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await api.post('blog/create', { text });
      navigate('/posts');
    } catch (error) {
      setError('Failed to create post');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h1>Create Post</h1>
      {error && <div className="alert alert-danger">{error}</div>}
      <div className="form-group">
        <label>Text</label>
        <textarea
          className="form-control"
          value={text}
          onChange={(event) => setText(event.target.value)}
          required
        />
      </div>
      <button type="submit" className="btn btn-primary">
        Create
      </button>
    </form>
  );
};

export default PostCreate;