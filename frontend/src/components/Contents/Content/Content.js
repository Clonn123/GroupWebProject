import React from 'react';
import './Content.css';
import { Link } from 'react-router-dom';

function Content({ cont }) {
  return (
    
      <div class="container">
      <div class="hoverable">
      <Link className='Link' to="/some-page">
      <div className="item">
        <img src={cont.url_img} alt={cont.title} />
        <h2 className='h2Item' >{cont.title}</h2>
        <p className='score'>{cont.score}</p>  
        <p>{cont.descriptionEpisod}</p>
        <p>{cont.descriptionData}</p>
      </div>
      </Link>
    <span class="hover-content">Контент, который появится при наведении</span>
    </div>
    </div>
  );
}

export default Content;