import React from 'react';

function ShikimoriButton() {
  return (
      <a
          className='oauth-button'
          href='https://shikimori.one/oauth/authorize?client_id=krfXoP58e9I2LpvUArHfdmkx1yUrBjgpoPbQTut0hDI&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fprofile&response_type=code&scope=user_rates+topics'
          style={{
            color: '#170600',
            border: '1.5px solid #170600',
            background: 'none',
            padding: '8px 16px',
            borderRadius: '5px',
            transition: 'background-color 0.3s, color 0.3s, border-color 0.3s',
            textDecoration: 'none',
            fontSize: '14px',
            width: '90px',
            marginBottom: '15px',
            cursor: 'pointer',
          }}
            // Добавляем стили для псевдокласса :hover
            onMouseEnter={(e) => {
              e.target.style.backgroundColor = '#95393c';
              e.target.style.borderColor = '#95393c';
              e.target.style.color = '#fff';
              e.target.style.opacity = '0.9';
          }}
          onMouseLeave={(e) => {
              e.target.style.backgroundColor = 'transparent';
              e.target.style.borderColor = '#170600';
              e.target.style.color = '#170600';
              e.target.style.opacity = '1';
          }}
      >
          Авторизоваться на shikimori
      </a>
  );
}

export default ShikimoriButton;