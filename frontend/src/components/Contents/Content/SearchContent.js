import React, { useState, useEffect, useRef} from "react";
import { Link, useNavigate } from 'react-router-dom';
import "./SearchContent.css";
import axios from "axios";

function SearchContent({ cont }) {

  return (
    <div> 
      <div class="SearchContent">
        <Link className="Link" to={`/mangas/${cont.manga_list_id}`}>
          <div className="item">
            <img src={cont.url_img} alt={cont.title_ru} />
            <div className="smolInfoContainer">
              <h2 className="h2Item">{cont.title_ru}</h2>
              <p className="score">{cont.score}</p>
              <p>{cont.descriptionEpisod}</p>
              <p>{cont.descriptionData}</p>
            </div>
            <div className="allInfoContainer">Инфа</div>
          </div>
        </Link>
      </div>
    </div>
  );
}

export default SearchContent;
