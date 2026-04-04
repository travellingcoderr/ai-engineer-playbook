import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { 
  Send, 
  Bot, 
  User, 
  Search, 
  Database, 
  ClipboardCheck, 
  Loader2,
  ChevronRight,
  ShieldCheck
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import './App.css';

interface Message {
  role: 'user' | 'assistant' | 'tool' | 'developer';
  content: string;
  tool_calls?: any[];
}

const App: React.FC = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [trace, setTrace] = useState<any[]>([]);
  const [isClaimModalOpen, setIsClaimModalOpen] = useState(false);
  
  // New Claim Form State
  const [newClaim, setNewClaim] = useState({
    claimId: '',
    patientName: '',
    status: 'pending',
    code: 'D1110',
    description: 'Prophylaxis - Adult'
  });

  const scrollRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMsg: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);
    setTrace([]);

    // START STREAMING
    try {
      const assistantMsg: Message = { role: 'assistant', content: '' };
      setMessages(prev => [...prev, assistantMsg]);
      
      const response = await fetch(`http://localhost:3003/api/v1/chat/stream?message=${encodeURIComponent(input)}`);
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) throw new Error("No reader");

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.slice(6);
            if (dataStr === '[DONE]') break;
            
            try {
              const data = JSON.parse(dataStr);
              if (data.type === 'content') {
                setMessages(prev => {
                  const newMsgs = [...prev];
                  const last = newMsgs[newMsgs.length - 1];
                  last.content += data.delta;
                  return newMsgs;
                });
              } else if (data.type === 'tool_start') {
                setTrace(prev => [...prev, { tool_calls: [{ name: data.tool }] }]);
              } else if (data.type === 'tool_end') {
                setTrace(prev => [...prev, { role: 'tool', output: data.output }]);
              }
            } catch (e) { /* ignore parse errors for partial chunks */ }
          }
        }
      }
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: "Sorry, I'm having trouble connecting to the streaming service." 
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setTrace([{ role: 'system', content: `Ingesting PDF: ${file.name}...` }]);

    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('http://localhost:3001/api/v1/ingestion/pdf', formData);
      setTrace(prev => [...prev, { role: 'system', content: 'PDF Vectorized Successfully!' }]);
      setMessages(prev => [...prev, { role: 'assistant', content: `Successfully ingested "${file.name}". I can now answer questions based on this policy!` }]);
    } catch (error) {
      setTrace(prev => [...prev, { role: 'system', content: 'Error during PDF ingestion.' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleAddClaim = async () => {
    setLoading(true);
    try {
      await axios.post('http://localhost:3002/api/v1/claims', {
        claimId: newClaim.claimId,
        patientName: newClaim.patientName,
        status: newClaim.status,
        procedures: [{
          code: newClaim.code,
          description: newClaim.description
        }]
      });
      setIsClaimModalOpen(false);
      setMessages(prev => [...prev, { role: 'assistant', content: `Successfully created claim ${newClaim.claimId} for ${newClaim.patientName}. You can now ask me about its status!` }]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <div className="chat-section">
        <header className="chat-header">
          <Bot className="trace-icon" />
          <h1>InsureDoc AI Dashboard</h1>
          
          <div style={{ marginLeft: 'auto', display: 'flex', gap: '12px', alignItems: 'center' }}>
            <button onClick={() => setIsClaimModalOpen(true)} className="action-btn">
              <ClipboardCheck size={16} /> New Claim
            </button>
            <button 
              onClick={() => fileInputRef.current?.click()}
              className="action-btn"
              title="Upload Policy PDF"
            >
              <Search size={16} /> Ingest PDF
            </button>
            <input 
              type="file" 
              ref={fileInputRef} 
              onChange={handleFileUpload} 
              style={{ display: 'none' }} 
              accept=".pdf"
            />
            <div style={{ opacity: 0.6, fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '5px' }}>
              <ShieldCheck size={14} /> SECURE AGENTIC FLOW
            </div>
          </div>
        </header>

        <main className="message-list" ref={scrollRef}>
          <AnimatePresence>
            {messages.map((msg, i) => (
              <motion.div 
                key={i}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`message ${msg.role === 'user' ? 'user' : 'ai'}`}
              >
                <div className="msg-header">
                  {msg.role === 'user' ? <User size={14} /> : <Bot size={14} />}
                  <span>{msg.role === 'user' ? 'You' : 'InsureDoc AI'}</span>
                </div>
                {msg.content}
              </motion.div>
            ))}
          </AnimatePresence>
          {loading && (
            <div className="thinking">
              <Loader2 className="animate-spin" size={16} /> 
              InsureDoc is analyzing claims and policies...
            </div>
          )}
        </main>

        <footer className="chat-controls">
          <div className="input-wrapper">
            <input 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask about a claim or policy (e.g., 'Why is CLAIM-123 stuck?')"
            />
            <button onClick={handleSend} className="send-btn">
              <Send size={18} />
            </button>
          </div>
        </footer>
      </div>

      <aside className="trace-sidebar">
        <h2 className="trace-header">Reasoning Trace</h2>
        <div className="trace-list">
          {trace.length === 0 && !loading && (
            <div style={{ opacity: 0.4, fontSize: '0.8rem', textAlign: 'center', marginTop: '40px' }}>
              No active reasoning trace. Ask a question to see the AI's internal flow.
            </div>
          )}
          {trace.map((step, i) => (
            <motion.div 
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: i * 0.1 }}
              key={i} 
              className="trace-item active"
            >
              {step.tool_calls ? <Search className="trace-icon" /> : <ClipboardCheck className="trace-icon" />}
              <div>
                <div style={{ fontWeight: 600 }}>{step.tool_calls ? 'Tool Identified' : 'Data Retrieved'}</div>
                <div style={{ opacity: 0.7, fontSize: '0.75rem', marginTop: '4px' }}>
                  {step.tool_calls?.[0]?.name === 'checkClaimStatus' && "Checking MongoDB Snapshot..."}
                  {step.tool_calls?.[0]?.name === 'searchInsurancePolicy' && "Searching Qdrant Vector Store..."}
                  {step.role === 'tool' && "Tool Execution Complete"}
                </div>
              </div>
            </motion.div>
          ))}
          {loading && trace.length === 0 && (
            <div className="trace-item active">
              <Database className="trace-icon animate-pulse" />
              <div>
                <div style={{ fontWeight: 600 }}>Analyzing Request</div>
                <div style={{ opacity: 0.7, fontSize: '0.8rem' }}>Route identified. Preparing tool calls...</div>
              </div>
            </div>
          )}
        </div>
      </aside>

      {/* NEW CLAIM MODAL */}
      <AnimatePresence>
        {isClaimModalOpen && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="modal-overlay"
          >
            <motion.div 
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              className="modal-content"
            >
              <h2>Add New Insurance Claim</h2>
              <div className="form-grid">
                <div className="form-group">
                  <label>Claim ID</label>
                  <input 
                    placeholder="e.g. CLAIM-999"
                    value={newClaim.claimId}
                    onChange={e => setNewClaim({...newClaim, claimId: e.target.value})}
                  />
                </div>
                <div className="form-group">
                  <label>Patient Name</label>
                  <input 
                    placeholder="e.g. John Doe"
                    value={newClaim.patientName}
                    onChange={e => setNewClaim({...newClaim, patientName: e.target.value})}
                  />
                </div>
                <div className="form-group">
                  <label>Current Status</label>
                  <select 
                    value={newClaim.status}
                    onChange={e => setNewClaim({...newClaim, status: e.target.value})}
                  >
                    <option value="pending">Pending</option>
                    <option value="stuck">Stuck</option>
                    <option value="processed">Processed</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Procedure Code</label>
                  <input 
                    placeholder="e.g. D1110"
                    value={newClaim.code}
                    onChange={e => setNewClaim({...newClaim, code: e.target.value})}
                  />
                </div>
                <div className="form-group" style={{ gridColumn: 'span 2' }}>
                  <label>Procedure Description</label>
                  <input 
                    placeholder="e.g. Routine Cleaning"
                    value={newClaim.description}
                    onChange={e => setNewClaim({...newClaim, description: e.target.value})}
                  />
                </div>
              </div>
              <div className="modal-actions">
                <button className="action-btn" onClick={() => setIsClaimModalOpen(false)}>Cancel</button>
                <button className="send-btn" onClick={handleAddClaim} disabled={loading}>
                  {loading ? 'Saving...' : 'Create Claim'}
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default App;
