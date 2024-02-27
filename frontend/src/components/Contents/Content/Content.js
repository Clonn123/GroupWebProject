import React from 'react';
import './Content.css';

function Content({ cont }) {
  return (
      <div className="item">
        <img src={cont.url_img} alt={cont.title} />
        <h2 className='h2Item' >{cont.title}</h2>
        <p>{cont.score}</p>  
        <p>{cont.descriptionEpisod}</p>
        <p>{cont.descriptionData}</p>       
      </div>
  );
}

export default Content;