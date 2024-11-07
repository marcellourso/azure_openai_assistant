import React from 'react';

function ResponseBox({ responses }) {
  return (
    <div className="response-box">
      {responses.map((response, index) => (
        <div key={index} className="response">
          {typeof response === 'string' ? response : JSON.stringify(response)} {/* Converte eventuali oggetti in stringhe per il debug */}
        </div>
      ))}
    </div>
  );
}

export default ResponseBox;
