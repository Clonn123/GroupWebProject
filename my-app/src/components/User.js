import React from 'react';
import '../css/UserList.css';

function User({ user }) {
  return (
    <div className="user-container">
        <div className="user">
            <p>Имя: {user.name}</p>
            <p>Фамилия: {user.surname}</p>
            <p>Логин: {user.username}</p>
            <p>Пароль: {user.password}</p>
            <p>Email: {user.email}</p>
        </div>
    </div>
  );
}

export default User;
