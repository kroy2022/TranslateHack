import { PrettyChatWindow } from 'react-chat-engine-pretty';
import React, {useState} from 'react';
import axios from 'axios';

const ChatsPage = (props) => {
    // Define a function to handle new messages
    const handleNewMessage = async (message) => {
        try {
            // Make a POST request to your backend API endpoint with the new message
            const response = await axios.post('http://localhost:3001/translateMessage', {
              message: message.text,
            });
      
            // Extract the translated message from the response
            const translatedMessage = response.data.translated_message;
      
            // Update the state with the modified message
            setMessages((prevMessages) => [...prevMessages, { ...message, text: translatedMessage }]);
      
            console.log('Translated Message:', translatedMessage);
          } catch (error) {
            console.error('Error sending message to the backend:', error);
          }
    };

    return (
        <div className="background">
          <div className="chat-wrapper">
            <PrettyChatWindow
              projectId={import.meta.env.VITE_CHAT_ENGINE_PROJECT_ID}
              username={props.user.username}
              secret={props.user.secret}
              onNewMessage="Dog" // Set the onNewMessage callback
            />
          </div>
        </div>
      );

}

export default ChatsPage;