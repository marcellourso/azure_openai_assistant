import React from 'react';

function Sidebar({ selectedThread, setSelectedThread }) {
  const handleUpload = (event) => {
    // Implementazione del caricamento file
  };

  return (
    <div className="sidebar">
      <select
        onChange={(e) => setSelectedThread(e.target.value)}
        value={selectedThread || ""}
      >
        {/* Opzioni del menu a discesa per i thread */}
      </select>
      <div className="file-previews">
        {/* Anteprime dei file */}
      </div>
      <button onClick={() => document.getElementById('fileUpload').click()}>
        Carica File
      </button>
      <input type="file" id="fileUpload" style={{ display: 'none' }} multiple onChange={handleUpload} />
    </div>
  );
}

export default Sidebar;