import React from 'react';

function ResponseBox({ responses }) {
  return (
    <div className="response-box">
      {responses.map((response, index) => (
        <p key={index}>{response}</p>
      ))}
    </div>
  );
}

export default ResponseBox;
