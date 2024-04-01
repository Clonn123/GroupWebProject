import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

import './LoginForm.css';

function LoginForm({ users, onLogin }) {
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      axios.post('http://127.0.0.1:8000/api/login/', {
        username: login,
        password: password,
      }).then((response) => {
        // Получаем access токен из ответа
        const accessToken = response.data.access_token;

        onLogin(accessToken, rememberMe);
      })
      .catch(error => {
        console.error('Ошибка:', error);
      });;

      // Если успешно вошли, перенаправляем пользователя на страницу профиля
      navigate('/profile');
    } catch (error) {
      // В случае ошибки выводим сообщение об ошибке
      setError('Неверный логин или пароль');
    }
  };

  return (
    <div className="login-form">
      <h2>Форма авторизации</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Логин"
          value={login}
          onChange={(e) => setLogin(e.target.value)}
        />
        <input
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <label>
          <input
            type="checkbox"
            checked={rememberMe}
            onChange={(e) => setRememberMe(e.target.checked)}
          />
          Запомнить меня
        </label>
        <button type="submit">Войти</button>
        {error && <p className="error-message">{error}</p>}
        <p>Нет аккаунта? <Link to="/registration">Зарегистрируйтесь</Link></p>
      </form>
      {/* <style>
        {`
          html {
            height: 100%;
            margin: 0 auto;
            font-family: 'Montserrat', sans-serif;
          }
        `}
      </style> */}
    </div>
  );
}

export default LoginForm;