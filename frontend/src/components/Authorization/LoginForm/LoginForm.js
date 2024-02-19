import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './LoginForm.css';

function LoginForm({ users, onLogin }) {
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const navigate = useNavigate(); //Это необходимо для перехода на страницу профиля после авторизации. useNavigate заменило useHistory

  const handleSubmit = (event) => {
    event.preventDefault();

    // Поиск пользователя с введенным логином и паролем
    const user = users.find(u => u.username === login && u.password === password);

    if (user) {
        onLogin(user, rememberMe);
        // Перенаправляем пользователя на страницу профиля
        navigate('/profile');
    } else {
      alert('Неверный логин или пароль');
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
        <p>Нет аккаунта? <Link to="/registration">Зарегистрируйтесь</Link></p>
      </form>
    </div>
  );
}

export default LoginForm;
