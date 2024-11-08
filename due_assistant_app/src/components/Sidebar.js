import React, { useState } from 'react';
import FilePreview from './FilePreview';
import './Sidebar.css'; // importa css della sidebar

function Sidebar({ threads, selectedThread, setSelectedThread }) {
  const [files, setFiles]=useState([]);

  const handleSelectChange = (e) => {
    const threadId = e.target.value;
    console.log("Thread ID selezionato:", threadId); // Verifica l'ID selezionato
    const selected = threads.find(thread => thread.id === threadId);
    console.log("Thread trovato:", selected); // Verifica il thread trovato
    setSelectedThread(selected); // Aggiorna selectedThread con il thread selezionato
  };

  const handleFileUpload = (e) => {
    const uploadedFiles = Array.from(e.target.files);
    setFiles(prevFiles => [...prevFiles, ...uploadedFiles]);
  };

  return (
    <div className="sidebar">
      <select
        onChange={handleSelectChange}
        value={selectedThread ? selectedThread.id : ""}
      >
        <option value="">Seleziona un thread</option>
        {threads.map(thread => (
          <option key={thread.id} value={thread.id}>
            {thread.title}
          </option>
        ))}
      </select>
        {/* Componente FilePreview per mostrare i file caricati */}
      <FilePreview files={files} />

      {/* Bottone di Upload in fondo */}
      <div className="upload-button">
        <input 
          type="file" 
          multiple 
          onChange={handleFileUpload}
          style={{ display: 'none' }}
          id="file-upload"
        />
        <label htmlFor="file-upload" className="upload-label">Upload Files</label>
      </div>

    </div>
  );
}

export default Sidebar;
