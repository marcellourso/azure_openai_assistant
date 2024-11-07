import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatBox from './components/ChatBox';
import ResponseBox from './components/ResponseBox';
import './App.css';

function App() {
  const [threads, setThreads] = useState([]); // Stato per la lista dei thread
  const [selectedThread, setSelectedThread] = useState(null);
  const [responses, setResponses] = useState([]);

  useEffect(() => {
    console.log("Thread selezionato:", selectedThread); // Debug per verificare se il thread selezionato cambia
  }, [selectedThread]);


  return (
    <div className="app">
      <Sidebar
        threads={threads}  
        selectedThread={selectedThread}
        setSelectedThread={setSelectedThread}
      />
      <div className="chat-container"> 
      <ResponseBox responses={responses} />
        <ChatBox 
          selectedThread={selectedThread} 
          setResponses={setResponses} 
          setThreads={setThreads}        // Passa setThreads a ChatBox
        />
      </div>
    </div>
  );
}

export default App;
