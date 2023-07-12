import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import Post from './Post';
import Swal from 'sweetalert2';

const Posts = () => {
  const [posts, setPosts] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await api.get('blog/');
        setPosts(response.data);
      } catch (error) {
        navigate('/login');
      }
    };
    fetchPosts();
  }, [navigate]);

  const handleUpdatePost = async (postId, newText) => {
    try {
      await api.patch(`blog/${postId}/`, { text: newText });
      const updatedPosts = posts.map((post) => {
        if (post.id === postId) {
          return { ...post, text: newText };
        } else {
          return post;
        }
      });
      setPosts(updatedPosts);
    } catch (error) {
      Swal.fire('Alert!', "You can't edit other's post!", 'error');
    }
  };

  const handleDeletePost = async (postId) => {
    try {
      await api.delete(`blog/${postId}/`);
      const updatedPosts = posts.filter((post) => post.id !== postId);
      setPosts(updatedPosts);
    } catch (error) {
      Swal.fire('Alert!', "You can't edit other's post!", 'error');
    }
  };

  const handleLike = async (postId) => {
    const response = await api.post(`blog/${postId}/like/`);
    const updatedPosts = posts.map((post) => {
      if (post.id === postId) {
        return { ...post, likes: response.data.count };
      }
      return post;
    });
    setPosts(updatedPosts);
  };

  return (
    <div>
      <h1>Posts</h1>
      <Link to="/posts/create" className="btn btn-primary mb-3">
        Create Post
      </Link>
      {posts.map((post) => (
        <Post
          key={post.id}
          post={post}
          onUpdatePost={handleUpdatePost}
          onDeletePost={handleDeletePost}
          onLike={handleLike}
        />
      ))}
    </div>
  );
};

export default Posts;