import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

import './LoginForm.css';

function LoginForm({ onLogin }) {
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
        const accessToken = response.data.access_token;
        if (accessToken != null) {
          // Проверяем, нужно ли запомнить пользователя
          if (rememberMe) {
            localStorage.setItem('accessToken', accessToken); //Не стоит ложить токен авторизации?
            console.log('Положили в хранилище')
          }
          onLogin(accessToken);
        }
        console.log('Идентификатор:', response.data.access_token);
      })
      .catch(error => {
        console.error('Ошибка:', error);
      });;

      console.log('Авторизация прошла');
      // Если успешно вошли, перенаправляем пользователя на страницу профиля
      navigate('/profile');
    } catch (error) {
      // В случае ошибки выводим сообщение об ошибке
      setError('Invalid username or password');
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
    </div>
  );
}

export default LoginForm;