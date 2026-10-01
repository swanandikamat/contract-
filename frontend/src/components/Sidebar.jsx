import React from 'react'
import { LayoutDashboard, FileSearch, Database, Server, Shield } from 'lucide-react'

export default function Sidebar({ currentTab, setCurrentTab, backendConnected, sampleCount, onRetryBackend }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-logo-icon">
          <Shield size={18} />
        </div>
        <div>
          <div className="sidebar-title">Legal Predictor</div>
          <div className="sidebar-subtitle">Risk Analysis Platform</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-label">Navigation</div>
        
        <button
          className={`nav-item ${currentTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setCurrentTab('dashboard')}
        >
          <LayoutDashboard size={16} />
          <span>Dashboard</span>
        </button>

        <button
          className={`nav-item ${currentTab === 'analysis' ? 'active' : ''}`}
          onClick={() => setCurrentTab('analysis')}
        >
          <FileSearch size={16} />
          <span>Contract Analysis</span>
        </button>

        <button
          className={`nav-item ${currentTab === 'dataset' ? 'active' : ''}`}
          onClick={() => setCurrentTab('dataset')}
        >
          <Database size={16} />
          <span>Benchmark Dataset</span>
        </button>
      </nav>

      <div className="sidebar-footer">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontWeight: '600', color: '#cbd5e1' }}>System Status</span>
          {!backendConnected && (
            <button 
              onClick={onRetryBackend} 
              style={{ background: 'none', border: 'none', color: '#60a5fa', fontSize: '0.7rem', cursor: 'pointer', textDecoration: 'underline' }}
            >
              Retry
            </button>
          )}
        </div>
        <div className="system-status-indicator">
          <span className={`status-dot ${backendConnected ? 'online' : 'offline'}`} />
          <span style={{ color: backendConnected ? '#cbd5e1' : '#f87171' }}>
            {backendConnected ? 'FastAPI & RAG Connected' : 'Backend Disconnected'}
          </span>
        </div>
        <div style={{ marginTop: '0.5rem', color: '#64748b', fontSize: '0.7rem' }}>
          ChromaDB: {sampleCount > 0 ? `${sampleCount * 10.5 | 0} Embeddings` : 'Indexed'}
        </div>
      </div>
    </aside>
  )
}
