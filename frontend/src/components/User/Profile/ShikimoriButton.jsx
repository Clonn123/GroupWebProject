import React from 'react';

function ShikimoriButton() {
  return (
    <a className="oauth-button" href="https://shikimori.one/oauth/authorize?client_id=krfXoP58e9I2LpvUArHfdmkx1yUrBjgpoPbQTut0hDI&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fprofile&response_type=code&scope=user_rates+topics">Авторизоваться на shikimori</a>
  );
}

export default ShikimoriButton;
