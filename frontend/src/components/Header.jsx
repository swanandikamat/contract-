import React from 'react'
import { AlertTriangle } from 'lucide-react'

export default function Header({ currentTab, backendConnected, activeFilename }) {
  const getHeaderInfo = () => {
    switch (currentTab) {
      case 'analysis':
        return {
          title: activeFilename ? `Contract Analysis: ${activeFilename}` : 'Contract Analysis Workspace',
          desc: 'Clause-level semantic risk detection, grounded evidence quotes, and RAG redlines'
        }
      case 'dataset':
        return {
          title: 'Benchmark Dataset Inventory',
          desc: '20 Standard reference contracts (10 CLEAN, 10 PROB) indexed in ChromaDB vector store'
        }
      case 'dashboard':
      default:
        return {
          title: 'Legal Risk Dashboard',
          desc: 'Contract risk analysis overview and benchmark dataset evaluation'
        }
    }
  }

  const info = getHeaderInfo()

  return (
    <header className="top-header">
      <div>
        <h1 className="page-header-title">{info.title}</h1>
        <p className="page-header-desc">{info.desc}</p>
      </div>

      <div className="header-actions">
        {!backendConnected && (
          <div className="badge badge-high" style={{ padding: '0.35rem 0.65rem' }}>
            <AlertTriangle size={13} />
            <span>Backend Offline (http://127.0.0.1:8000)</span>
          </div>
        )}
      </div>
    </header>
  )
}
