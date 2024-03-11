import "./PageContent.css";
import { useParams } from "react-router-dom";
import React, { useState, useEffect } from "react";
import axios from "axios";
import RatingComponent from "../SettintContent/RatingComponent.js";
import ReviewComponent from "../SettintContent/ReviewComponent.js";
import plox from './plox.png';

const PageContent = ({ currentUser }) => {
  const { id } = useParams();
  const [infoList, setInfoList] = useState();
  const [isLoading, setIsLoading] = useState(true);
  useEffect(() => {
    if (!currentUser || !currentUser.id) {
      return; 
    }
    setIsLoading(true);
    axios
      .get(`http://127.0.0.1:8000/api/info/anime/?id_user=${currentUser.id}&id_anime=${id}`)
      .then((response) => {
        setInfoList(response.data);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error("Ошибка:", error);
        setIsLoading(false);
      });
  }, []);
  
  return (
    <>
    <div className="page-content"> 
    {isLoading && <div>Loading...</div>}
    {!isLoading && infoList && (
        <>
          <h2 className="anime_title">
            {infoList.anime_info2.title_ru} / {infoList.anime_info2.title_en}
          </h2>
          <div className="anime-details">
            <div>
              <img
                className="anime-image"
                src={infoList.anime_info2.url_img}
                alt={infoList.anime_info2.title_ru}
              />
            </div>
            <div className="infoA"> <h4>Информация</h4> 
              <p className="anime-description">
                <strong>Тип:</strong>  {infoList.anime_info2.descriptionEpisod}
              </p>
              <p><strong>Эпизоды:</strong> {infoList.anime_info.Episodes}</p>
              <p className="anime-description">
                <strong>Дата:</strong> {infoList.anime_info2.descriptionData}
              </p>
              <p><strong>Жанры:</strong> {infoList.anime_info.Genres}</p>
              <p><strong>Темы:</strong> {infoList.anime_info.Themes}</p>
            </div>
            <div className="infoB">
              <div className="additional-info"><strong>Оценки других пользователей</strong></div>
            </div>
          </div>
          <div className="SettintContent">
            <RatingComponent currentUser={currentUser} info={infoList.anime_info3}/>
            <ReviewComponent currentUser={currentUser} info={infoList.anime_info3}/>
          </div>
        </>
      )}
    </div>
    </>
    
  );
};

export default PageContent;
