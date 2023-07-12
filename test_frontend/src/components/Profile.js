import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { logout } from '../auth';
import api from '../api';

const Profile = () => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await api.get('user/');
        setUser(response.data);
      } catch (err) {
        logout();
        navigate('/login');
      }
    };
    fetchUser();
  }, [navigate]);

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Profile</h1>
      <p>Username: {user.username}</p>
      <p>Email: {user.email}</p>
      <p>Location: {user.userprofile.location}</p>
      <p>Login Date: {user.userprofile.date}</p>
      <p>Ip Address: {user.userprofile.ip_address}</p>
    </div>
  );
};

export default Profile;