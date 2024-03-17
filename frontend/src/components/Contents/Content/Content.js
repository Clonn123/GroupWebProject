import React, { useState, useEffect, useRef} from "react";
import { Link, useNavigate } from 'react-router-dom';
import "./Content.css";
import axios from "axios";

function Content({ cont, selectedIcon, currentUser }) {
  const [isWatched, setScoreList] = useState();

  useEffect(() => {
    axios
      .get(
        `http://127.0.0.1:8000/api/anime/?id_user=${currentUser.id}&id_anime=${cont.anime_list_id}`
      )
      .then((response) => {
        setScoreList(response.data);
      })
      .catch((error) => {
        console.error("Ошибка:", error);
      });
  }, [currentUser.id, cont.anime_list_id]);

  

  return (
    <div
      className={`${selectedIcon === "infoSort" ? "selected" : "no_selected"}`}
    > 
      <div class="hoverable">
        <Link className="Link" to={`/animes/${cont.anime_list_id}`}>
          <div className="item">
            <img src={cont.url_img} alt={cont.title_ru} />

            {isWatched && (
              <div className="watched-icons-container">
                {isWatched=="completed" && <div className="watched-icon param1"></div>}
                {isWatched=="planned" && <div className="watched-icon param2"></div>}
                {isWatched=="dropped" && <div className="watched-icon param3"> </div>}
                {isWatched=="watching" && <div className="watched-icon param4"> </div>}
              </div>
            )}
            <div className="smolInfoContainer">
              <h2 className="h2Item">{cont.title_ru}</h2>
              <p className="score">{cont.score}</p>
              <p>{cont.descriptionEpisod}</p>
              <p>{cont.descriptionData}</p>
            </div>
            <div className="allInfoContainer">Инфа</div>
          </div>
        </Link>
        <span class="hover-content">
          <p className="">{cont.title_ru}</p>
          <p className="score">{cont.score}</p>
          <p>{cont.descriptionEpisod}</p>
          <p>{cont.descriptionData}</p>

        </span>
      </div>
    </div>
  );
}

export default Content;
