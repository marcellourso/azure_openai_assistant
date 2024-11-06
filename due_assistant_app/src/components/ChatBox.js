import React, { useState } from 'react';
import Modal from 'react-modal';
import { FaPaperPlane, FaPlus } from 'react-icons/fa';
import { createThread } from '../services/api';

Modal.setAppElement('#root'); // Necessario per l'accessibilità con react-modal

function ChatBox({ selectedThread, setResponses, setThreads }) {
  const [message, setMessage] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newThreadTitle, setNewThreadTitle] = useState("");

  // Funzione per inviare il messaggio
  const handleSendMessage = async () => {
    if (selectedThread) {
      const response = await sendMessage(selectedThread.id, message);
      setResponses(prevResponses => [...prevResponses, response]);
      setMessage("");
    } else {
      alert("Seleziona un thread prima di inviare un messaggio.");
    }
  };

  // Funzione per aprire la modale per creare un nuovo thread
  const handleOpenModal = () => {
    setIsModalOpen(true);
  };

  // Funzione per chiudere la modale
  const handleCloseModal = () => {
    setIsModalOpen(false);
    setNewThreadTitle("");
  };

  // Funzione per creare un nuovo thread
  const handleCreateThread = async () => {
    if (newThreadTitle.trim()) {
      const newThread = await createThread(newThreadTitle);
      setThreads(prevThreads => [...prevThreads, newThread]);
      setIsModalOpen(false);
      setNewThreadTitle("");
    } else {
      alert("Inserisci un nome valido per il thread.");
    }
  };

  return (
    <div className="chat-box">
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Scrivi il tuo messaggio..."
      />
      <div className="buttons">
        <button onClick={handleSendMessage}><FaPaperPlane /></button>
        <button onClick={handleOpenModal}><FaPlus /></button>
      </div>

      {/* Modale per inserire il nome del thread */}
      <Modal
        isOpen={isModalOpen}
        onRequestClose={handleCloseModal}
        contentLabel="Crea un nuovo thread"
        className="modal"
        overlayClassName="overlay"
      >
        <h2>Crea un nuovo thread</h2>
        <input
          type="text"
          value={newThreadTitle}
          onChange={(e) => setNewThreadTitle(e.target.value)}
          placeholder="Nome del thread"
        />
        <button onClick={handleCreateThread}>Crea</button>
        <button onClick={handleCloseModal}>Annulla</button>
      </Modal>
    </div>
  );
}

export default ChatBox;
