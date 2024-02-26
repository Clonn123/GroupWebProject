import React from 'react';
import './Content.css';

function Content({ cont }) {
  return (
      <div className="item">
        <img src={cont.url_img} alt={cont.title} />
        <h2>{cont.title}</h2>
        <p>{cont.description}</p>     
      </div>
  );
}

export default Content;