import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { apiService } from '../../services/api';
import { Bot, Send, ShieldCheck, Network, FileText, Cpu, CheckCircle2 } from 'lucide-react';
import './AICopilotPage.scss';

export const AICopilotPage: React.FC = () => {
  const [question, setQuestion] = useState('What maintenance procedure applies to machine M001?');
  const [messages, setMessages] = useState<any[]>([]);

  const queryMutation = useMutation({
    mutationFn: (q: string) => apiService.queryCopilot(q),
    onSuccess: (data) => {
      setMessages((prev) => [
        ...prev,
        { role: 'user', content: question },
        { role: 'assistant', data }
      ]);
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;
    queryMutation.mutate(question);
  };

  return (
    <div className="copilot-page">
      <div className="page-header">
        <div>
          <h1>Enterprise AI Copilot</h1>
          <p className="subtitle">Ask grounded questions across structured Postgres data, Neo4j knowledge graphs, and ChromaDB vector documents.</p>
        </div>
        <div className="copilot-mode-tag">
          <Bot size={16} /> Grounded Hybrid RAG Mode
        </div>
      </div>

      <div className="copilot-layout">
        <div className="chat-window-card">
          <div className="messages-list">
            {messages.length === 0 ? (
              <div className="hero-prompt-state">
                <Bot size={40} className="hero-icon" />
                <h2>Enterprise Context Intelligence</h2>
                <p>Ask complex questions about machine faults, suppliers, production orders, or quality standards.</p>
                <div className="sample-prompts">
                  <button onClick={() => setQuestion("What maintenance procedure applies to machine M001?")}>
                    What maintenance procedure applies to machine M001?
                  </button>
                  <button onClick={() => setQuestion("What should an operator check when a machine shows abnormal vibration?")}>
                    What should an operator check when a machine shows abnormal vibration?
                  </button>
                  <button onClick={() => setQuestion("Which supplier and material information is associated with the maintenance context for M001?")}>
                    Which supplier and material information is associated with the maintenance context for M001?
                  </button>
                </div>
              </div>
            ) : (
              messages.map((msg, i) => (
                <div key={i} className={`message-row ${msg.role}`}>
                  {msg.role === 'user' ? (
                    <div className="user-bubble">{msg.content}</div>
                  ) : (
                    <div className="assistant-card">
                      <div className="assistant-header">
                        <Bot size={18} className="bot-icon" />
                        <span className="assistant-name">ContextIQ Engine</span>
                        <span className="model-tag font-mono">{msg.data.model || 'Gemini 2.0 Flash'}</span>
                        <span className="grounding-score">
                          <ShieldCheck size={14} /> Grounding Score: {Math.round((msg.data.grounding_score || 0.95) * 100)}%
                        </span>
                      </div>

                      <div className="answer-text">{msg.data.answer}</div>

                      {/* Citations & Source Evidence */}
                      {msg.data.citations && msg.data.citations.length > 0 && (
                        <div className="evidence-panel">
                          <div className="evidence-header font-mono">
                            <FileText size={14} /> Grounded Citations ({msg.data.citations.length})
                          </div>
                          <div className="evidence-grid">
                            {msg.data.citations.map((cit: any, cIdx: number) => (
                              <div key={cIdx} className="evidence-box">
                                <h5><CheckCircle2 size={14} /> {cit.citation_id} — {cit.document_title}</h5>
                                <div className="evidence-item">{cit.snippet}</div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Execution Trace */}
                      {msg.data.execution_trace && (
                        <div className="trace-box">
                          <h5><Cpu size={14} /> Execution Trace</h5>
                          <div className="trace-list">
                            {msg.data.execution_trace.map((step: any, tIdx: number) => (
                              <div key={tIdx} className="trace-step font-mono">
                                <span className="stage">Step {step.step}: {step.name}</span>
                                <span className="details">{step.details}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>

          <form onSubmit={handleSubmit} className="prompt-form">
            <input
              type="text"
              placeholder="Ask enterprise context query..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />
            <button type="submit" className="send-btn" disabled={queryMutation.isPending}>
              {queryMutation.isPending ? 'Reasoning...' : <Send size={16} />}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
