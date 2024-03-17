import React, { useState, useEffect, useRef} from "react";
import { Link, useNavigate } from 'react-router-dom';
import "./Content.css";
import axios from "axios";

function ContentRec({ cont }) {
  const [isWatched, setScoreList] = useState();

  return (
    <div>
        <div className={"no_selected"}>
      <div class="hoverable">
        <Link className="Link" to={`/animes/${cont.anime_id}`}>
          <div className="item">
            <img src={cont.url_img} alt={cont.title_ru} />
            <div className="smolInfoContainer">
              <h2 className="h2Item">{cont.title_ru}</h2>
              <p className="score">{cont.score_real}</p>
              <p>{cont.type}</p>
              <p>{cont.data}</p>
            </div>
            <div className="allInfoContainer">Инфа</div>
          </div>
        </Link>
        <span class="hover-content">
          <p className="">{cont.title_ru}</p>
          <p className="score">{cont.score_real}</p>
          <p>{cont.type}</p>
          <p>{cont.data}</p>
        </span>
      </div>
    </div>
    </div> 
  );
}

export default ContentRec;