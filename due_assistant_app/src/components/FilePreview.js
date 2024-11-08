// src/components/FilePreview.js
import React from 'react';
import './FilePreview.css';

function FilePreview({ files }) {
  return (
    <div className="file-preview">
      {files.map((file, index) => (
        <div key={index} className="file-thumbnail">
          {file.name} {/* Visualizza il nome del file */}
        </div>
      ))}
    </div>
  );
}

export default FilePreview;
