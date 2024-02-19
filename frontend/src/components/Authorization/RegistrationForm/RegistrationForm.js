import './RegistrationForm.css';

import React, { useState } from "react";
import { Link } from 'react-router-dom';

function RegistrationForm({ onUserAdd }) {
    const [email, setEmail] = useState('');
    const [name, setName] = useState('');
    const [surname, setSurname] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
  
    const handleSubmit = (event) => {
      event.preventDefault(); // Предотвращаем стандартное поведение отправки формы
  
      // Создаем нового пользователя
      const newUser = {
        id: Math.random(), // Генерируем уникальный идентификатор
        email,
        name,
        surname,
        username,
        password,
      };
  
      // Добавляем нового пользователя в список пользователей
      onUserAdd(newUser);
  
      // Сбрасываем значения полей формы
      setEmail('');
      setName('');
      setSurname('');
      setUsername('');
      setPassword('');
    };
  
    return (
      <div className="registration-form">
        <h2>Форма регистрации</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="E-mail"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="text"
            placeholder="Имя"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <input
            type="text"
            placeholder="Фамилия"
            value={surname}
            onChange={(e) => setSurname(e.target.value)}
          />
          <input
            type="text"
            placeholder="Логин (никнейм)"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            placeholder="Пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="submit">Зарегистрироваться</button>
        </form>
        <p>Уже есть аккаунт? <Link to="/login">Войдите</Link></p>
      </div>
    );
  }

export default RegistrationForm;