import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import ChatBox from './components/ChatBox';
import ResponseBox from './components/ResponseBox';
import './App.css';

function App() {
  const [selectedThread, setSelectedThread] = useState(null);
  const [responses, setResponses] = useState([]);

  return (
    <div className="app">
      <Sidebar
        selectedThread={selectedThread}
        setSelectedThread={setSelectedThread}
      />
      <div className="chat-container">
        <ResponseBox responses={responses} />
        <ChatBox selectedThread={selectedThread} setResponses={setResponses} />
      </div>
    </div>
  );
}

export default App;
