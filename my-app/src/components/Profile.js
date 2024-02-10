import React from 'react';

function Profile({ currentUser, onLogout }) {
  return (
    <div>
      <p>Добро пожаловать, {currentUser.name}!</p>
      <button onClick={onLogout}>Выйти</button>
    </div>
  );
}

export default Profile;