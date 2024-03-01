import React, { useState } from "react";
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

import './RegistrationForm.css';

function RegistrationForm() {
    const [email, setEmail] = useState('');
    const [name, setName] = useState('');
    const [surname, setSurname] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [gender, setGender] = useState('other');
    const [age, setAge] = useState('');
    const [birthdate, setBirthdate] = useState('');
    const [error, setError] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const [showModal, setShowModal] = useState(false); // Состояние для отслеживания видимости модального окна
    const navigate = useNavigate();
  
    const handleSubmit = async (event) => {
      event.preventDefault(); // Предотвращаем стандартное поведение отправки формы

      if (!email || !name || !surname || !username || !password || !gender || !birthdate) {
        setError('Пожалуйста, заполните все поля');
        return;
      }
  
    try {
      // Проверяем, существует ли пользователь с такой почтой
      const emailExist = await axios.post('http://127.0.0.1:8000/api/check-email/', { email });
      if (emailExist.data) {
        setError('Пользователь с этой почтой уже существует');
        return;
      }
      // Проверяем, существует ли пользователь с таким логином
      const usernameExist = await axios.post('http://127.0.0.1:8000/api/check-username/', { username });
      if (usernameExist.data) {
        setError('Пользователь с этим логином уже существует');
        return;
      }

      axios.post('http://127.0.0.1:8000/api/register/', {
          email,
          name,
          surname,
          username,
          password,
          gender,
          birthdate
      }).then((response) => {
        
      // Успешно зарегистрирован
      setSuccessMessage('Пользователь успешно создан');
      setShowModal(true); // Показать модальное окно
      })
      .catch(error => {
        console.error('Ошибка при регистрации:', error);
        setSuccessMessage('');
      });;
    } catch (error) {
    }
  };

  const closeModal = () => {
    setShowModal(false); // Скрыть модальное окно
    navigate('/login'); // Перейти на страницу входа
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
          <select
              value={gender}
              onChange={(e) => setGender(e.target.value)}
          >
              <option value="Другой">Другой</option>
              <option value="Мужской">Мужской</option>
              <option value="Женский">Женский</option>              
          </select>
          {/* <input
              type="number"
              placeholder="Возраст"
              value={age}
              onChange={(e) => setAge(e.target.value)}
          /> */}
          <input
              type="date"
              placeholder="Дата рождения"
              value={birthdate}
              onChange={(e) => setBirthdate(e.target.value)}
          />
          <button type="submit">Зарегистрироваться</button>
          {error && <p className="error-message">{error}</p>}
          <p>Уже есть аккаунт? <Link to="/login">Войдите</Link></p>
        </form>
        {/* Модальное окно */}
        {showModal && (
          <div className="modal">
            <div className="modal-content">
              <span className="close" onClick={closeModal}>&times;</span>
              <p className="success-message">{successMessage}</p>
              <button className="modal-button" onClick={closeModal}>OK</button>
            </div>
          </div>
        )}
      </div>
    );
  }

export default RegistrationForm;