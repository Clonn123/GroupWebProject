import "./PageContent.css";
import { useParams } from "react-router-dom";
import React, { useState, useEffect } from "react";
import axios from "axios";
import RatingComponent from "../SettintContent/RatingComponent.js";
import StatusComponent from "../SettintContent/StatusComponent.js";
import plox from './plox.png';

const PageContent = () => {
  const { id } = useParams();
  const [infoList, setInfoList] = useState();
  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/info/anime/" + id)
      .then((response) => {
        setInfoList(response.data);
      })
      .catch((error) => {
        console.error("Ошибка:", error);
      });
  }, []);

  return (
    <div className="page-content">
      {infoList && (
        <>
          <h2 className="anime_title">
            {infoList.anime_info2.title_en} / {infoList.anime_info2.title_en}
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
                Тип: {infoList.anime_info2.descriptionEpisod}
              </p>
              <p>Эпизоды: {infoList.anime_info.Episodes}</p>
              <p className="anime-description">
                Дата: {infoList.anime_info2.descriptionData}
              </p>
              <p>Жанры: {infoList.anime_info.Genres}</p>
              <p>Темы: {infoList.anime_info.Themes}</p>
            </div>
            <div className="infoB">
              <div className="additional-info">Да я вор, Плох?</div>
              <img className="plox" src={plox} />
            </div>
          </div>
        </>
      )}
      <RatingComponent />
      <StatusComponent />
    </div>
  );
};

export default PageContent;
