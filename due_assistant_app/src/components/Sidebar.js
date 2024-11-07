import React from 'react';

function Sidebar({ threads, selectedThread, setSelectedThread }) {
  const handleSelectChange = (e) => {
    const threadId = e.target.value;
    console.log("Thread ID selezionato:", threadId); // Verifica l'ID selezionato

    const selected = threads.find(thread => thread.id === threadId);
    console.log("Thread trovato:", selected); // Verifica il thread trovato

    setSelectedThread(selected); // Aggiorna selectedThread con il thread selezionato
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
    </div>
  );
}

export default Sidebar;
