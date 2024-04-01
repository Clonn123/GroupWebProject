import React, { useContext } from 'react';
import { ProfileContext} from './context';
import ava from './ava.jpg';

function Avatar( {photoUrl} ) {
  const imageCtx = useContext(ProfileContext);

  return (
    <>
    <div className="avatar">
      <img src={imageCtx.userImage || ava} />
    </div>
    </>
    
  );
}

export default Avatar;