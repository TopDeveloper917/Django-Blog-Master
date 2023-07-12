import React, { useState } from 'react';

function Post({ post, onUpdatePost, onDeletePost, onLike }) {
  const [isEditing, setIsEditing] = useState(false);
  const [text, setText] = useState(post.text);

  function handleEdit() {
    setIsEditing(true);
  }

  function handleCancel() {
    setIsEditing(false);
    setText(post.text);
  }

  async function handleSave() {
    await onUpdatePost(post.id, text);
    setIsEditing(false);
  }

  async function handleDelete() {
    await onDeletePost(post.id);
  }

  function handleLike() {
    onLike(post.id);
  }

  return (
    <div className="card mb-3">
      <div className="card-body">
        <h5 className="card-title">{post.user.username}</h5>
        {isEditing ? (
          <div>
            <textarea
              className="form-control mb-2"
              value={text}
              onChange={(event) => setText(event.target.value)}
            />
            <button className="btn btn-primary mr-2" onClick={handleSave}>
              Save
            </button>
            <button className="btn btn-secondary" onClick={handleCancel}>
              Cancel
            </button>
          </div>
        ) : (
          <p className="card-text">{post.text}</p>
        )}
        <button className="btn btn-link" onClick={handleLike}>
          Like ({Array.isArray(post.likes) ? post.likes.length : post.likes})
        </button>
        <button className="btn btn-link" onClick={handleEdit}>
          Edit
        </button>
        <button className="btn btn-link" onClick={handleDelete}>
          Delete
        </button>
      </div>
    </div>
  );
}

export default Post;