import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; // Используем Routes вместо Switch
import Header from './components/header.js';
import './css/App.css';
import RegistrationForm from './components/RegistrationForm.js';
import ContentList from './components/contentList.js';
import UserList from './components/UserList.js';

function App() {
  const [users, setUsers] = useState([
    { id: 1, name: 'Артем', surname: 'Полозников', username: 'Clonn123', password: 'Clonn123', email: 'art-clon@mail.ru' },
    { id: 2, name: 'Андрей', surname: 'Смирнов', username: 'Gifon', password: 'Gifon', email: 'gifon@mail.ru' },
  ]);
  const dataList = [
    { 
      imageUrl: 'https://desu.shikimori.one/uploads/poster/animes/52991/preview_alt-f180ae801fddf9551e27aff2d96f2112.jpeg',
      title: 'Название1',
      description: 'Описание1',
    },
    { 
      imageUrl: 'https://desu.shikimori.one/uploads/poster/animes/52991/preview_alt-f180ae801fddf9551e27aff2d96f2112.jpeg',
      title: 'Название2',
      description: 'Описание2',
    },
    { 
      imageUrl: 'https://desu.shikimori.one/uploads/poster/animes/52991/preview_alt-f180ae801fddf9551e27aff2d96f2112.jpeg',
      title: 'Название2',
      description: 'Описание2',
    },
    { 
      imageUrl: 'https://desu.shikimori.one/uploads/poster/animes/52991/preview_alt-f180ae801fddf9551e27aff2d96f2112.jpeg',
      title: 'Название2',
      description: 'Описание2',
    },
    { 
      imageUrl: 'https://desu.shikimori.one/uploads/poster/animes/52991/preview_alt-f180ae801fddf9551e27aff2d96f2112.jpeg',
      title: 'Название2',
      description: 'Описание2',
    },
    { 
      imageUrl: 'https://desu.shikimori.one/uploads/poster/animes/52991/preview_alt-f180ae801fddf9551e27aff2d96f2112.jpeg',
      title: 'Название2',
      description: 'Описание2',
    },
    { 
      imageUrl: 'https://desu.shikimori.one/uploads/poster/animes/52991/preview_alt-f180ae801fddf9551e27aff2d96f2112.jpeg',
      title: 'Название2',
      description: 'Описание2',
    },
    { 
      imageUrl: 'https://desu.shikimori.one/uploads/poster/animes/52991/preview_alt-f180ae801fddf9551e27aff2d96f2112.jpeg',
      title: 'Название2',
      description: 'Описание2',
    },
    { 
      imageUrl: 'https://desu.shikimori.one/uploads/poster/animes/52991/preview_alt-f180ae801fddf9551e27aff2d96f2112.jpeg',
      title: 'Название2',
      description: 'Описание2',
    },
  ];

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
          <Route path="/animes" element={<ContentList dataList={dataList}  />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
