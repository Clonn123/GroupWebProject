import "./PageContent.css";
import { useParams } from "react-router-dom";
import React, { useState, useEffect } from "react";
import axios from "axios";
import RatingComponent from "../SettintContent/RatingComponentManga.js";
import ReviewComponent from "../SettintContent/ReviewComponent.js";

const PageContentManga = ({ currentUser }) => {
  const { id } = useParams();
  const [infoList, setInfoList] = useState();
  const [isLoading, setIsLoading] = useState(true);
  useEffect(() => {
    if (!currentUser || !currentUser.id) {
      return; 
    }
    setIsLoading(true);

    axios
      .get(`http://127.0.0.1:8000/api/info/manga/?id_user=${currentUser.id}&id_manga=${id}`)
      .then((response) => {
        setInfoList(response.data);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error("Ошибка:", error);
        setIsLoading(false);
      });
  }, [currentUser, id]);
  
  return (
    <>
    <div className="page-content"> 
    {isLoading && <h2>Loading...</h2>}
    {!isLoading && infoList && (
        <>
          <h2 className="anime_title">
            {infoList.manga_info2.title_ru} / {infoList.manga_info2.title_en}
          </h2>
          <div className="anime-details">
            <div>
              <img
                className="anime-image"
                src={infoList.manga_info2.url_img}
                alt={infoList.manga_info2.title_ru}
              />
            </div>
            <div className="infoA"> <h4>Информация:</h4> 
              <p className="anime-description">
                <strong>Тип:</strong>  {infoList.manga_info2.descriptionEpisod}
              </p>
              <p><strong>Эпизоды:</strong> {infoList.manga_info.Episodes}</p>
              <p className="anime-description">
                <strong>Дата:</strong> {infoList.manga_info2.descriptionData}
              </p>
              <p><strong>Жанры:</strong> {infoList.manga_info.Genres}</p>
              <p><strong>Темы:</strong> {infoList.manga_info.Themes}</p>
              <p><strong>Студия:</strong> {infoList.manga_info2.studios}</p>
            </div>
            <div className="infoB">
              <div className="additional-info"><h4>Рейтинг:</h4></div>
              <p>Оценка нашего сайта: <strong>{infoList.score}</strong> </p>
              <a className="a" href={`https://shikimori.one/mangas/${infoList.manga_info2.manga_list_id}`}>
                Shikimori: <strong>{infoList.manga_info2.score}</strong>
              </a>
            </div>
            <style>
        {`
          html {
            height: 100%;
            margin: 0 auto;
            font-family: 'Montserrat', sans-serif;
          }
        `}
      </style>
          </div>
          <div className="SettintContent">
            <RatingComponent currentUser={currentUser} info={infoList.manga_info3}/>
            <ReviewComponent currentUser={currentUser} info={infoList.manga_info3}/>
          </div>
        </>
      )}
    </div>
    </>
    
  );
};

export default PageContentManga;
