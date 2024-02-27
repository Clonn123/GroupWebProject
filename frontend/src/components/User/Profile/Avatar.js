import React, { useContext } from 'react';
import { ProfileContext} from './context';

function Avatar( {photoUrl} ) {
  const imageCtx = useContext(ProfileContext);

  return (
    <div className="avatar">
      <img src={imageCtx.userImage || "https://img.icons8.com/color/400/name--v1.png"} alt="name--v1"/>
    </div>
  );
}

export default Avatar;