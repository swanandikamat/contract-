import React, { useState } from 'react'
import { Search, Play } from 'lucide-react'

export default function DatasetView({ samples = [], onAnalyze, setSelectedSample, loading }) {
  const [filterCategory, setFilterCategory] = useState('ALL')
  const [searchQuery, setSearchQuery] = useState('')

  const cleanCount = samples.filter(s => s.category === 'CLEAN').length
  const probCount = samples.filter(s => s.category === 'PROB').length

  const filteredSamples = samples.filter(s => {
    if (filterCategory === 'CLEAN' && s.category !== 'CLEAN') return false
    if (filterCategory === 'PROB' && s.category !== 'PROB') return false
    if (searchQuery.trim()) {
      return s.filename.toLowerCase().includes(searchQuery.toLowerCase())
    }
    return true
  })

  return (
    <div>
      <div className="panel">
        <div className="panel-header">
          <div className="panel-title">Benchmark Dataset Catalog</div>
          <span className="badge badge-neutral">{samples.length} Benchmark Files Indexed</span>
        </div>
        <div className="panel-body">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: '0.75rem' }}>
            <div className="filter-tabs" style={{ marginBottom: 0 }}>
              <button
                className={`tab-btn ${filterCategory === 'ALL' ? 'active' : ''}`}
                onClick={() => setFilterCategory('ALL')}
              >
                All Contracts ({samples.length})
              </button>
              <button
                className={`tab-btn ${filterCategory === 'CLEAN' ? 'active' : ''}`}
                onClick={() => setFilterCategory('CLEAN')}
              >
                CLEAN ({cleanCount})
              </button>
              <button
                className={`tab-btn ${filterCategory === 'PROB' ? 'active' : ''}`}
                onClick={() => setFilterCategory('PROB')}
              >
                PROB ({probCount})
              </button>
            </div>

            <div style={{ position: 'relative', width: '260px' }}>
              <Search size={14} style={{ position: 'absolute', left: '0.6rem', top: '0.55rem', color: '#94a3b8' }} />
              <input
                type="text"
                className="form-input"
                style={{ paddingLeft: '2rem', fontSize: '0.8rem' }}
                placeholder="Search benchmark files..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>

          <div className="table-container">
            <table className="enterprise-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Contract Filename</th>
                  <th>Category</th>
                  <th>Relative Data Path</th>
                  <th style={{ textAlign: 'right' }}>Action</th>
                </tr>
              </thead>
              <tbody>
                {filteredSamples.length === 0 ? (
                  <tr>
                    <td colSpan={5} style={{ textAlign: 'center', padding: '2rem', color: '#94a3b8' }}>
                      No benchmark files match your search filter.
                    </td>
                  </tr>
                ) : (
                  filteredSamples.map((s, idx) => (
                    <tr key={s.filename}>
                      <td style={{ color: '#94a3b8', fontSize: '0.75rem' }}>{idx + 1}</td>
                      <td style={{ fontWeight: '600', color: '#0f172a' }}>{s.filename}</td>
                      <td>
                        {s.category === 'CLEAN' ? (
                          <span className="badge badge-clean">CLEAN (Low Risk)</span>
                        ) : (
                          <span className="badge badge-high">PROB (High Risk)</span>
                        )}
                      </td>
                      <td style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: '#64748b' }}>
                        {s.relative_path}
                      </td>
                      <td style={{ textAlign: 'right' }}>
                        <button
                          className="btn btn-secondary btn-sm"
                          onClick={() => {
                            setSelectedSample(s.filename)
                            onAnalyze(s.filename)
                          }}
                          disabled={loading}
                        >
                          <Play size={12} />
                          <span>Run RAG Analysis</span>
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}
