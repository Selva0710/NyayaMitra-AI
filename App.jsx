import React, { useState } from 'react';
import Sidebar from './components/Layout/Sidebar';
import Header from './components/Layout/Header';
import ChatInterface from './components/Chat/ChatInterface';
import { chatService } from './services/api';

function App() {
    const [language, setLanguage] = useState('en');
    const [messages, setMessages] = useState([]);
    const [isTyping, setIsTyping] = useState(false);
    const [sessionHistory, setSessionHistory] = useState([
        { id: 1, title: 'GST Registration Query' },
        { id: 2, title: 'Draft Non-Disclosure Agreement' }
    ]);
    const [currentSession, setCurrentSession] = useState(null);

    const handleSendMessage = async (text, agentType = 'auto', file = null) => {
        // 1. Add User Message
        const userMsg = { role: 'user', content: text, file: file };
        setMessages(prev => [...prev, userMsg]);
        setIsTyping(true);

        try {
            // Check if there is an active session id
            const currentSessionId = currentSession ? currentSession.id : null;

            const response = await chatService.sendMessage(text, agentType, currentSessionId);

            const botMsg = {
                role: 'assistant',
                content: response.content || "Error getting response."
            };
            setMessages(prev => [...prev, botMsg]);

            // Auto-set title if new session
            if (!currentSession) {
                const newTitle = text.substring(0, 25) + '...';
                const newSession = { id: response.session_id || Date.now(), title: newTitle };
                setCurrentSession(newSession);
                setSessionHistory(prev => [newSession, ...prev]);
            }
        } catch (error) {
            console.error("Failed to fetch from backend:", error);
            const errorMsg = {
                role: 'assistant',
                content: "**Error:** Could not connect to the FastAPI backend. Please ensure the backend is running on `http://localhost:8000`."
            };
            setMessages(prev => [...prev, errorMsg]);
        } finally {
            setIsTyping(false);
        }
    };

    const handleFileUpload = (file) => {
        handleSendMessage(`Please analyze this document: ${file.name}`, 'document', file);
    };

    const createNewChat = () => {
        setMessages([]);
        setCurrentSession(null);
    };

    return (
        <div className="flex h-screen bg-dark overflow-hidden font-sans">
            <div className="hidden md:block">
                <Sidebar
                    history={sessionHistory}
                    createNewChat={createNewChat}
                    currentSession={currentSession}
                />
            </div>

            <div className="flex-1 flex flex-col h-full relative">
                <Header language={language} setLanguage={setLanguage} />

                <main className="flex-1 overflow-hidden relative">
                    <ChatInterface
                        messages={messages}
                        isTyping={isTyping}
                        onSendMessage={handleSendMessage}
                        onFileUpload={handleFileUpload}
                    />
                </main>
            </div>
        </div>
    );
}

export default App;
