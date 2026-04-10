import { useState } from 'react'
import { Shield, MessageSquare, Send, X, Paperclip, Maximize2, Minimize2, Loader2 } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import './App.css'
import products from './data/products'
import FormMessage from './components/FormMessage'

function App() {
  const [isChatOpen, setIsChatOpen] = useState(false)
  const [messages, setMessages] = useState([
    { text: "Namaste! I am your Insurance Advisor. How can I help you today?", isBot: true }
  ])
  const [input, setInput] = useState("")
  const [sessionId] = useState(() => Math.random().toString(36).substring(7))
  const [selectedFile, setSelectedFile] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isMaximized, setIsMaximized] = useState(false)

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onloadend = () => {
      setSelectedFile({
        name: file.name,
        mimeType: file.type,
        base64: reader.result.split(',')[1]
      });
    };
    reader.readAsDataURL(file);
  }

  const handleSend = async (overrideText) => {
    const textToSend = typeof overrideText === 'string' ? overrideText : input;
    if (!textToSend.trim() && !selectedFile) return
    
    const userMessage = { text: textToSend, isBot: false };
    if (selectedFile) {
      userMessage.file = selectedFile.name;
    }
    
    setMessages(prev => [...prev, userMessage]);
    setInput("")
    setIsLoading(true)
    
    const parts = [];
    if (textToSend.trim()) {
      parts.push({ text: textToSend });
    }
    if (selectedFile) {
      parts.push({
        inline_data: {
          mime_type: selectedFile.mimeType,
          data: selectedFile.base64
        }
      });
    }
    
    setSelectedFile(null);
    
    try {
      const response = await fetch('https://insurance-advisor-1058427839055.us-central1.run.app/run', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          app_name: "insurance_advisor",
          user_id: "web_user",
          session_id: sessionId,
          new_message: {
            role: "user",
            parts: parts
          }
        }),
      });
      
      const events = await response.json();
      
      const agentEvent = events.reverse().find(e => e.author !== 'user' && e.content && e.content.parts);
      
      if (agentEvent && agentEvent.content.parts[0].text) {
        setMessages(prev => [...prev, { 
          text: agentEvent.content.parts[0].text, 
          isBot: true 
        }])
      } else {
        setMessages(prev => [...prev, { 
          text: "I received your message but couldn't generate a response. Please try again.", 
          isBot: true 
        }])
      }
    } catch (error) {
      console.error("Error calling agent:", error);
      setMessages(prev => [...prev, { 
        text: "Sorry, I am having trouble connecting to the server.", 
        isBot: true 
      }])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="app-container light-theme">
      {/* Header */}
      <header className="header">
        <div className="logo">
          <Shield size={24} color="#00b4d8" />
          <span>Secure Life</span>
        </div>
        <nav className="nav">
          <a href="#products">Insurance Products</a>
          <a href="#renew">Renew Your Policy</a>
          <a href="#claim">Claim</a>
          <a href="#support">Support</a>
          <button className="btn-outline">Talk to Expert</button>
          <button className="btn-primary">Sign in</button>
        </nav>
      </header>
 
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <h1>Let's find you the <span>Best Insurance</span></h1>
          <p>Quick, easy & hassle free • 51 insurers offering competitive prices</p>
          <div className="hero-buttons">
            <button className="btn-large">View Plans</button>
          </div>
        </div>
        <div className="hero-banner">
          <img src="/hero_banner_wide.png" alt="Secure Life Banner" />
        </div>
      </section>
 
      {/* Insurance Categories Grid */}
      <section id="products" className="categories-section">
        <div className="products-grid">
          {products.map((product, index) => (
            <div key={index} className="product-card" style={{ borderTopColor: product.color }}>
              <div className="product-icon" style={{ color: product.color }}>
                {product.icon}
              </div>
              <h3>{product.name}</h3>
            </div>
          ))}
        </div>
        <div style={{ textAlign: 'center', marginTop: '2rem' }}>
          <button className="btn-outline">View all products</button>
        </div>
      </section>
 
      {/* Chat Widget */}
      <div className={`chat-widget ${isChatOpen ? 'open' : ''}`}>
        {isChatOpen ? (
          <div className={`chat-window ${isMaximized ? 'maximized' : ''}`}>
            <div className="chat-header">
              <div className="chat-title">
                <Shield size={24} color="#fff" />
                <span>Insurance Advisor</span>
              </div>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button className="btn-close" onClick={() => setIsMaximized(!isMaximized)}>
                  {isMaximized ? <Minimize2 size={20} color="#fff" /> : <Maximize2 size={20} color="#fff" />}
                </button>
                <button className="btn-close" onClick={() => setIsChatOpen(false)}>
                  <X size={20} color="#fff" />
                </button>
              </div>
            </div>
            <div className="chat-messages">
              {messages.map((msg, index) => {
                const formRegex = /\[FORM:\s*(.+?)\]/;
                const match = msg.text.match(formRegex);
                
                if (match && msg.isBot) {
                  const fields = match[1].split(',').map(f => f.trim());
                  const textWithoutForm = msg.text.replace(formRegex, '');
                  
                  return (
                    <FormMessage 
                      key={index} 
                      text={textWithoutForm} 
                      fields={fields} 
                      onSubmit={(data) => {
                        const formattedData = Object.entries(data).map(([k, v]) => `${k}: ${v}`).join(', ');
                        handleSend(formattedData);
                      }}
                    />
                  );
                }
                
                return (
                  <div key={index} className={`message ${msg.isBot ? 'bot' : 'user'}`}>
                    <ReactMarkdown>{msg.text}</ReactMarkdown>
                    {msg.file && (
                      <div className="message-file" style={{ fontSize: '0.8rem', marginTop: '0.25rem', opacity: 0.8 }}>
                        📎 {msg.file}
                      </div>
                    )}
                  </div>
                );
              })}
              {isLoading && (
                <div className="message bot" style={{ opacity: 0.7 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Loader2 className="spin" size={16} />
                    <span>Insurance Advisor is thinking...</span>
                  </div>
                </div>
              )}
            </div>
            <div className="chat-input-area">
              <input 
                type="file" 
                id="file-upload" 
                style={{ display: 'none' }} 
                onChange={handleFileChange}
                accept="image/*,video/*"
              />
              <button className="btn-icon" onClick={() => document.getElementById('file-upload').click()}>
                <Paperclip size={20} color="#666" />
              </button>
              <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                {selectedFile && (
                  <div className="file-preview" style={{ fontSize: '0.8rem', color: '#666', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span>📎 {selectedFile.name}</span>
                    <button style={{ border: 'none', background: 'transparent', cursor: 'pointer' }} onClick={() => setSelectedFile(null)}>
                      <X size={12} color="#ff4d6d" />
                    </button>
                  </div>
                )}
                <input 
                  type="text" 
                  placeholder="Ask me anything..." 
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                  style={{ width: '100%', border: 'none', outline: 'none' }}
                />
              </div>
              <button className="btn-icon" onClick={handleSend}>
                <Send size={20} color="#00b4d8" />
              </button>
            </div>
          </div>
        ) : (
          <button className="chat-btn" onClick={() => setIsChatOpen(true)}>
            <MessageSquare size={28} color="#fff" />
            <span className="chat-badge">1</span>
          </button>
        )}
      </div>
 
      {/* Footer */}
      <footer className="footer">
        <p>&copy; 2026 SecureLife Insurance. All rights reserved.</p>
      </footer>
    </div>
  )
}

export default App
