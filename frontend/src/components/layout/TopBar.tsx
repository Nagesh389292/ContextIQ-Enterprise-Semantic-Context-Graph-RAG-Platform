import React, { useState } from 'react';
import { Search, Bell, Sun, Moon, User, Command } from 'lucide-react';
import './TopBar.scss';

interface TopBarProps {
  theme: 'dark' | 'light';
  onToggleTheme: () => void;
  userEmail?: string;
}

export const TopBar: React.FC<TopBarProps> = ({ theme, onToggleTheme, userEmail = 'demo@contextiq.dev' }) => {
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <header className="app-topbar">
      <div className="topbar-search">
        <Search className="search-icon" size={16} />
        <input
          type="text"
          placeholder="Search enterprise context, machines, orders, documents... (Ctrl + K)"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <span className="kbd-shortcut"><Command size={12} /> K</span>
      </div>

      <div className="topbar-actions">
        <button className="icon-btn" onClick={onToggleTheme} title="Toggle Theme">
          {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
        </button>

        <button className="icon-btn" title="Notifications">
          <Bell size={18} />
          <span className="notification-dot" />
        </button>

        <div className="user-profile">
          <div className="avatar">
            <User size={16} />
          </div>
          <div className="user-info">
            <span className="user-name">Nagesh Reddy</span>
            <span className="user-role">Demo Environment</span>
          </div>
        </div>
      </div>
    </header>
  );
};
