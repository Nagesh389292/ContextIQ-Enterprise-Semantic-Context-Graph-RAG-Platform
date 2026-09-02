import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Lock, Mail, ShieldAlert, ArrowRight } from 'lucide-react';
import './LoginPage.scss';

export const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('demo@contextiq.dev');
  const [password, setPassword] = useState('demo');
  const navigate = useNavigate();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    // Demo authentication redirect
    navigate('/');
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="brand-header">
          <div className="logo-hex">◈</div>
          <h1>ContextIQ</h1>
          <p>Enterprise Semantic Context Engine</p>
        </div>

        <div className="demo-banner">
          <ShieldAlert size={16} /> DEMO ENVIRONMENT • Preset Credentials Below
        </div>

        <form onSubmit={handleLogin} className="login-form">
          <div className="form-group">
            <label>Email Address</label>
            <div className="input-with-icon">
              <Mail size={16} className="icon" />
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            </div>
          </div>

          <div className="form-group">
            <label>Password</label>
            <div className="input-with-icon">
              <Lock size={16} className="icon" />
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            </div>
          </div>

          <button type="submit" className="login-btn">
            Sign In to ContextIQ <ArrowRight size={16} />
          </button>
        </form>

        <div className="login-footer font-mono">
          Demo Account: demo@contextiq.dev / demo
        </div>
      </div>
    </div>
  );
};
