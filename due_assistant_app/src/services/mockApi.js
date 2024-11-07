// src/services/mockApi.js

  export const createThread = async (title) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ id: Date.now().toString(), title });
      }, 500);
    });
  };
  
  
  export const sendMessage = async (threadId, message) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ response: `Risposta simulata per: "${message}"` });
      }, 500);
    });
  };
  
