import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; // Используем Routes вместо Switch
import Header from './components/header.js';
import './css/App.css';
import RegistrationForm from './components/RegistrationForm.js';
import Content from './components/content.js';
import UserList from './components/UserList.js';

function App() {
  const [users, setUsers] = useState([
    { id: 1, name: 'Артем', surname: 'Полозников', username: 'Clonn123', password: 'Clonn123', email: 'art-clon@mail.ru' },
    { id: 2, name: 'Андрей', surname: 'Смирнов', username: 'Gifon', password: 'Gifon', email: 'gifon@mail.ru' },
  ]);

  const handleAddUser = (newUser) => {
    setUsers([...users, newUser]); // Добавляем нового пользователя в список
  };

  return (
    <Router>
      <div>
        <Header className="panel"/>
        <Routes>
          <Route path="/registration" element={<RegistrationForm onUserAdd={handleAddUser} />} />
          <Route path="/" element={<UserList users={users} />} />
          <Route path="/animes" element={<Content onUserAdd={handleAddUser} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
