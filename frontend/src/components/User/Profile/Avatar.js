import React from 'react';

function Avatar( {photoUrl} ) {

  return (
    <div className="avatar">
      <img width="200" height="200" src={photoUrl} alt="name--v1"/>
    </div>
  );
}

export default Avatar;