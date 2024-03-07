import './PageContent.css';
import { useParams } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import RatingComponent from '../SettintContent/RatingComponent.js'
import StatusComponent from '../SettintContent/StatusComponent.js'

const PageContent = () => {
  const { id } = useParams();
  const [infoList, setInfoList] = useState();
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/info/anime/'+id)
      .then(response => {
        setInfoList(response.data);
      })
      .catch(error => {
        console.error('Ошибка:', error);
      });
  }, []);



  return (
    <div>
      <h2>Страница элемента с id: {id}</h2>
      {infoList && (
  <div>
    <h2>Детали аниме</h2>
      <RatingComponent animeId={id} />
      <StatusComponent animeId={id} />
    <div>
        <img src={infoList.anime_info2.url_img} alt={infoList.anime_info2.title_ru} />
        <p>Название на русском: {infoList.anime_info2.title_ru}</p>
        <p>Название на английском: {infoList.anime_info2.title_en}</p>
        <p>Тип: {infoList.anime_info2.descriptionEpisod}</p>
        <p>Дата: {infoList.anime_info2.descriptionData}</p>
        <p>Оценка: {infoList.anime_info2.score}</p>
    </div>
    <h2>Дополнительная информация</h2>
    <div>
        <p>Эпизоды: {infoList.anime_info.Episodes}</p>
        <p>Жанры: {infoList.anime_info.Genres}</p>
        <p>Темы: {infoList.anime_info.Themes}</p>
    </div>
  </div>
)}
    </div>
  );
};

export default PageContent;