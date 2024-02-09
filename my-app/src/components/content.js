import React from 'react';
import '../css/content.css';

function Content({ cont }) {
  return (
      <div className="item">
        <img src={cont.imageUrl} alt={cont.title} />
        <h2>{cont.title}</h2>
        <p>{cont.description}</p>     
      </div>
  );
}

export default Content;