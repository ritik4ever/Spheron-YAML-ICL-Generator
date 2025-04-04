import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

// Import ace editor
import AceEditor from 'react-ace';
import 'ace-builds/src-noconflict/mode-yaml';
import 'ace-builds/src-noconflict/theme-github';

function App() {
  const [yaml, setYaml] = useState('');
  const [validation, setValidation] = useState({ valid: true, errors: [] });
  const [chatHistory, setChatHistory] = useState([]);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleUserInput = async (e) => {
    e.preventDefault();
    
    if (!message.trim()) return;
    
    // Add user message to chat history
    const newChatHistory = [...chatHistory, { user: true, text: message }];
    setChatHistory(newChatHistory);
    
    setLoading(true);
    try {
      let response;
      if (yaml) {
        // Refine existing YAML
        response = await axios.post('http://localhost:5000/api/refine-yaml', { 
          text: message, 
          current_yaml: yaml 
        });
      } else {
        // Generate new YAML
        response = await axios.post('http://localhost:5000/api/generate-yaml', { 
          text: message 
        });
      }
      
      setYaml(response.data.yaml);
      setValidation(response.data.validation);
      
      // Add system response to chat history
      setChatHistory([
        ...newChatHistory, 
        { user: false, text: 'I\'ve updated the YAML based on your request.' }
      ]);
    } catch (error) {
      console.error('Error processing request:', error);
      setChatHistory([
        ...newChatHistory,
        { user: false, text: 'Sorry, I encountered an error processing your request.' }
      ]);
    } finally {
      setLoading(false);
      setMessage('');
    }
  };
  
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Spheron YAML Generator</h1>
        <p>Describe your deployment requirements in natural language</p>
      </header>
      
      <div className="content-container">
        <div className="chat-panel">
          <div className="chat-messages">
            {chatHistory.length === 0 ? (
              <div className="welcome-message">
                <p>Welcome! Describe your deployment needs, for example:</p>
                <ul>
                  <li>"I need a Node.js service with 1GB memory and auto-scaling"</li>
                  <li>"Deploy a Python application with Redis"</li>
                </ul>
              </div>
            ) : (
              chatHistory.map((chat, index) => (
                <div 
                  key={index} 
                  className={`chat-message ${chat.user ? 'user-message' : 'system-message'}`}
                >
                  <div className="message-content">{chat.text}</div>
                </div>
              ))
            )}
          </div>
          
          <form className="chat-input-form" onSubmit={handleUserInput}>
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Describe your deployment requirements..."
              className="chat-input"
              disabled={loading}
            />
            <button 
              type="submit" 
              className="send-button"
              disabled={loading}
            >
              {loading ? 'Processing...' : 'Send'}
            </button>
          </form>
        </div>
        
        <div className="yaml-panel">
          <h2>Generated YAML Configuration</h2>
          <AceEditor
            mode="yaml"
            theme="github"
            value={yaml || '# Your YAML configuration will appear here'}
            name="yaml-editor"
            width="100%"
            height="400px"
            readOnly={true}
            editorProps={{ $blockScrolling: true }}
            setOptions={{
              showLineNumbers: true,
              tabSize: 2,
            }}
          />
          
          {validation.valid ? (
            <div className="validation valid">
              ✓ YAML configuration is valid
            </div>
          ) : (
            <div className="validation invalid">
              <div className="validation-header">⚠ YAML has issues:</div>
              <ul className="validation-errors">
                {validation.errors.map((error, index) => (
                  <li key={index}>{error}</li>
                ))}
              </ul>
            </div>
          )}
          
          <div className="yaml-actions">
            <button 
              className="copy-button"
              onClick={() => {
                navigator.clipboard.writeText(yaml);
                alert('YAML copied to clipboard!');
              }}
              disabled={!yaml}
            >
              Copy to clipboard
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;