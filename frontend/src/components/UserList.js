import React from 'react';
import User from './User';

function UserList({ users }) {
  return (
    <div>
      <h2 className="user-title">Список пользователей</h2>
      {users.map(user => (
        <User key={user.id} user={user} />
      ))}
    </div>
  );
}

export default UserList;
