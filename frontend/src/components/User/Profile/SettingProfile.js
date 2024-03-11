import React, { useState, useContext } from 'react';
import './SettingProfile.css';
import SaveButton from './Save';
import Avatar from './Avatar';
import { ProfileContext } from './context';
import axios from 'axios';


function SettingsPage( {currentUser} ) {
  const [photo, setPhoto] = useState('');
  const [nickname, setNickname] = useState(currentUser.username);
  const [firstName, setFirstName] = useState(currentUser.name);
  const [lastName, setLastName] = useState(currentUser.surname);
  const [gender, setGender] = useState(currentUser.gender);
  const [birthdate, setBirthdate] = useState(currentUser.age);
  const [previewPhoto, setPreviewPhoto] = useState(null);
  
  const imageCtx = useContext(ProfileContext);


  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      axios.put('http://127.0.0.1:8000/api/settings/', {
        username: nickname,
        name: firstName,
        surname: lastName,

      }).then((response) => {
      })
      .catch(error => {
      });;
    } catch (error) {
    }
  };
  

  const handlePhotoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      imageCtx.setUserImage(URL.createObjectURL(file));
      setPhoto(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewPhoto(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  

  return (
    <div className='settint-container'>
      <form className='formsetting' onSubmit={handleSubmit}>
      <h2>Настройки</h2>
        <div>
          <label htmlFor="photo">Фото:</label>
          <input type="file" id="photo" onChange={handlePhotoChange} />
        </div>
        <div>
          <label htmlFor="nickname">Никнейм:</label>
          <input type="text" id="nickname" value={nickname} onChange={(e) => setNickname(e.target.value)} />
        </div>
        <div>
          <label htmlFor="firstName">Имя:</label>
          <input type="text" id="firstName" value={firstName} onChange={(e) => setFirstName(e.target.value)} />
        </div>
        <div>
          <label htmlFor="lastName">Фамилия:</label>
          <input type="text" id="lastName" value={lastName} onChange={(e) => setLastName(e.target.value)} />
        </div>
        <div>
          <label htmlFor="gender">Пол:</label>
          <select id="gender" value={gender} onChange={(e) => setGender(e.target.value)}>
            <option value="Мужской">Мужской</option>
            <option value="Женский">Женский</option>
            <option value="Другой">Другой</option>
          </select>
        </div>
        <div>
          <label htmlFor="age">Возраст:</label>
          <input type="date" id="birthdate" value={birthdate} onChange={(e) => setBirthdate(e.target.value)} />
        </div>
        <button type="submit"> Сохранить </button>

      </form>
    </div>
  );
}

export default SettingsPage;
